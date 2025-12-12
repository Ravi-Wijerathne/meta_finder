#!/usr/bin/env python3
"""
Unified Build Script for MetaFinder - Linux
Builds all Linux distribution packages
"""

import sys
import os
import argparse

# Import build modules
try:
    from build_deb import build_deb
    from build_rpm import build_rpm
    from build_portable_linux import build_portable
except ImportError as e:
    print(f"Error importing build modules: {e}")
    print("Make sure all build scripts are in the same directory.")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description='Build MetaFinder packages for Linux distributions',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python build_all_linux.py --all              # Build all packages
  python build_all_linux.py --deb              # Build DEB package only
  python build_all_linux.py --rpm              # Build RPM package only
  python build_all_linux.py --portable         # Build portable version only
  python build_all_linux.py --deb --portable   # Build DEB and portable

Requirements:
  - Python 3.6+
  - PyInstaller: pip install pyinstaller
  - For DEB: dpkg-dev (apt-get install dpkg-dev)
  - For RPM: rpm-build (dnf install rpm-build)
        """
    )
    
    parser.add_argument('--all', action='store_true',
                        help='Build all package types')
    parser.add_argument('--deb', action='store_true',
                        help='Build DEB package (Ubuntu/Mint)')
    parser.add_argument('--rpm', action='store_true',
                        help='Build RPM package (Fedora)')
    parser.add_argument('--portable', action='store_true',
                        help='Build portable version')
    
    args = parser.parse_args()
    
    # If no arguments specified, show help
    if not (args.all or args.deb or args.rpm or args.portable):
        parser.print_help()
        sys.exit(0)
    
    # Determine what to build
    build_deb_pkg = args.all or args.deb
    build_rpm_pkg = args.all or args.rpm
    build_portable_pkg = args.all or args.portable
    
    print("=" * 70)
    print("MetaFinder Linux Build System")
    print("=" * 70)
    print("\nBuilding:")
    if build_deb_pkg:
        print("  ✓ DEB package (Ubuntu/Linux Mint/Debian)")
    if build_rpm_pkg:
        print("  ✓ RPM package (Fedora/RHEL/CentOS)")
    if build_portable_pkg:
        print("  ✓ Portable version (All Linux)")
    print()
    
    build_results = []
    
    # Build DEB package
    if build_deb_pkg:
        try:
            print("\n" + "█" * 70)
            print("BUILDING DEB PACKAGE")
            print("█" * 70 + "\n")
            build_deb()
            build_results.append(("DEB", True, None))
        except Exception as e:
            build_results.append(("DEB", False, str(e)))
            print(f"\n✗ DEB build failed: {e}")
    
    # Build RPM package
    if build_rpm_pkg:
        try:
            print("\n" + "█" * 70)
            print("BUILDING RPM PACKAGE")
            print("█" * 70 + "\n")
            build_rpm()
            build_results.append(("RPM", True, None))
        except Exception as e:
            build_results.append(("RPM", False, str(e)))
            print(f"\n✗ RPM build failed: {e}")
    
    # Build Portable version
    if build_portable_pkg:
        try:
            print("\n" + "█" * 70)
            print("BUILDING PORTABLE VERSION")
            print("█" * 70 + "\n")
            build_portable()
            build_results.append(("Portable", True, None))
        except Exception as e:
            build_results.append(("Portable", False, str(e)))
            print(f"\n✗ Portable build failed: {e}")
    
    # Print summary
    print("\n" + "=" * 70)
    print("BUILD SUMMARY")
    print("=" * 70)
    
    success_count = sum(1 for _, success, _ in build_results if success)
    total_count = len(build_results)
    
    for build_type, success, error in build_results:
        status = "✓ SUCCESS" if success else "✗ FAILED"
        print(f"  {build_type:15} {status}")
        if error:
            print(f"    Error: {error}")
    
    print()
    print(f"Completed: {success_count}/{total_count} builds successful")
    
    if success_count == total_count:
        print("\n🎉 All builds completed successfully!")
        print("\nGenerated files can be found in the 'dist' directory.")
        return 0
    else:
        print("\n⚠️  Some builds failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
