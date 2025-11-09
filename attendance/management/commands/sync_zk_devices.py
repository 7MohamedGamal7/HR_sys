"""
Django management command to sync ZK fingerprint devices
أمر إدارة Django لمزامنة أجهزة البصمة ZK
"""
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from attendance.zk_integration import (
    sync_all_devices, 
    test_device_connection,
    get_sync_status,
    get_configured_devices
)
from datetime import datetime, timedelta
import json


class Command(BaseCommand):
    help = 'Sync attendance data from ZK fingerprint devices | مزامنة بيانات الحضور من أجهزة البصمة'

    def add_arguments(self, parser):
        parser.add_argument(
            '--test',
            action='store_true',
            help='Test connection to all configured devices',
        )
        parser.add_argument(
            '--status',
            action='store_true',
            help='Show current sync status',
        )
        parser.add_argument(
            '--device',
            type=str,
            help='Test specific device (format: ip:port)',
        )
        parser.add_argument(
            '--days',
            type=int,
            default=None,
            help='Number of days to sync (default: all)',
        )
        parser.add_argument(
            '--no-process',
            action='store_true',
            help='Do not auto-process logs after sync',
        )
        parser.add_argument(
            '--list-devices',
            action='store_true',
            help='List all configured devices',
        )

    def handle(self, *args, **options):
        """Execute the command"""
        
        # List configured devices
        if options['list_devices']:
            self.list_devices()
            return
        
        # Show sync status
        if options['status']:
            self.show_status()
            return
        
        # Test specific device
        if options['device']:
            self.test_device(options['device'])
            return
        
        # Test all devices
        if options['test']:
            self.test_all_devices()
            return
        
        # Perform sync
        self.sync_devices(options)

    def list_devices(self):
        """List all configured devices"""
        self.stdout.write(self.style.HTTP_INFO('\n=== Configured ZK Devices ===\n'))
        
        devices = get_configured_devices()
        
        if not devices:
            self.stdout.write(self.style.WARNING('No devices configured'))
            self.stdout.write(
                '\nTo configure devices, add a SystemSettings record with:\n'
                '  Key: zk_devices\n'
                '  Value: name1|ip1:port1,name2|ip2:port2,...\n'
            )
            return
        
        for i, device in enumerate(devices, 1):
            self.stdout.write(
                f"{i}. {device['name']}\n"
                f"   IP: {device['ip']}\n"
                f"   Port: {device['port']}\n"
            )

    def show_status(self):
        """Show current sync status"""
        self.stdout.write(self.style.HTTP_INFO('\n=== Sync Status ===\n'))
        
        status = get_sync_status()
        
        self.stdout.write(f"Configured Devices: {status['devices_configured']}")
        self.stdout.write(f"Unprocessed Logs: {status['unprocessed_logs']}")
        
        if status['last_sync_time']:
            self.stdout.write(f"Last Sync: {status['last_sync_time']}")
        else:
            self.stdout.write("Last Sync: Never")
        
        if status['recent_attendance']:
            self.stdout.write('\nRecent Attendance Records:')
            for att in status['recent_attendance'][:5]:
                self.stdout.write(
                    f"  {att['employee']} - {att['date']} - {att['status']}"
                )

    def test_device(self, device_str):
        """Test connection to a specific device"""
        try:
            if ':' in device_str:
                ip, port = device_str.split(':', 1)
                port = int(port)
            else:
                ip = device_str
                port = 4370
            
            self.stdout.write(f'\nTesting connection to {ip}:{port}...\n')
            
            result = test_device_connection(ip, port)
            
            if result['success']:
                self.stdout.write(self.style.SUCCESS(f'✓ {result["message"]}'))
                
                if result['device_info']:
                    info = result['device_info']
                    self.stdout.write('\nDevice Information:')
                    self.stdout.write(f"  Serial Number: {info.get('serial_number', 'N/A')}")
                    self.stdout.write(f"  Platform: {info.get('platform', 'N/A')}")
                    self.stdout.write(f"  Firmware: {info.get('firmware_version', 'N/A')}")
                    self.stdout.write(f"  Device Time: {info.get('device_time', 'N/A')}")
                    self.stdout.write(f"  Users: {info.get('users_count', 0)}")
                    self.stdout.write(f"  Records: {info.get('records_count', 0)}")
            else:
                self.stdout.write(self.style.ERROR(f'✗ {result["message"]}'))
                if result['error']:
                    self.stdout.write(f'  Error: {result["error"]}')
                    
        except Exception as e:
            raise CommandError(f'Error testing device: {str(e)}')

    def test_all_devices(self):
        """Test connection to all configured devices"""
        self.stdout.write(self.style.HTTP_INFO('\n=== Testing All Devices ===\n'))
        
        devices = get_configured_devices()
        
        if not devices:
            self.stdout.write(self.style.WARNING('No devices configured'))
            return
        
        for device in devices:
            self.stdout.write(f"\nTesting {device['name']}...")
            result = test_device_connection(device['ip'], device['port'])
            
            if result['success']:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Connected'))
                if result['device_info']:
                    info = result['device_info']
                    self.stdout.write(f"  Users: {info.get('users_count', 0)}, Records: {info.get('records_count', 0)}")
            else:
                self.stdout.write(self.style.ERROR(f'  ✗ Failed: {result.get("error", "Unknown error")}'))

    def sync_devices(self, options):
        """Sync all devices"""
        self.stdout.write(self.style.HTTP_INFO('\n=== Starting ZK Device Sync ===\n'))
        
        # Calculate date range if specified
        start_date = None
        end_date = None
        
        if options['days']:
            end_date = timezone.now()
            start_date = end_date - timedelta(days=options['days'])
            self.stdout.write(f'Syncing last {options["days"]} days')
            self.stdout.write(f'From: {start_date}')
            self.stdout.write(f'To: {end_date}\n')
        
        # Perform sync
        auto_process = not options['no_process']
        
        try:
            results = sync_all_devices(start_date, end_date, auto_process)
            
            # Display results
            self.stdout.write('\n' + '='*50)
            self.stdout.write(self.style.SUCCESS('\nSync Completed!\n'))
            self.stdout.write('='*50 + '\n')
            
            self.stdout.write(f"Devices Synced: {results['devices_synced']}")
            self.stdout.write(f"Devices Failed: {results['devices_failed']}")
            self.stdout.write(f"Total Records Fetched: {results['total_fetched']}")
            self.stdout.write(f"New Records: {results['total_success']}")
            self.stdout.write(f"Duplicates: {results['total_duplicates']}")
            self.stdout.write(f"Errors: {results['total_errors']}")
            self.stdout.write(f"Invalid Records: {results['total_invalid']}")
            self.stdout.write(f"Employee Not Found: {results['total_employee_not_found']}")
            
            if results['processing_stats']:
                stats = results['processing_stats']
                self.stdout.write('\nProcessing Results:')
                self.stdout.write(f"  Logs Processed: {stats['processed_logs']}")
                self.stdout.write(f"  Attendance Created: {stats['created_attendance']}")
                self.stdout.write(f"  Attendance Updated: {stats['updated_attendance']}")
                self.stdout.write(f"  Processing Errors: {stats['errors']}")
            
            # Show device-specific results
            if results['device_results']:
                self.stdout.write('\nDevice Results:')
                for device_result in results['device_results']:
                    device_name = device_result['device']
                    status = device_result['status']
                    
                    if status == 'success':
                        stats = device_result['stats']
                        self.stdout.write(
                            f"  ✓ {device_name}: {stats['success']} new, "
                            f"{stats['duplicates']} duplicates, {stats['errors']} errors"
                        )
                    else:
                        error = device_result.get('error', 'Unknown error')
                        self.stdout.write(self.style.ERROR(f"  ✗ {device_name}: {error}"))
            
            self.stdout.write('\n' + '='*50 + '\n')
            
            if results['total_success'] > 0:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'\n✓ Successfully synced {results["total_success"]} new attendance records!\n'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING('\nNo new records to sync.\n')
                )
                
        except Exception as e:
            raise CommandError(f'Sync failed: {str(e)}')

