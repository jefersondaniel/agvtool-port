'''
Example usage:

agvtool new-version -all 1722
agvtool new-marketing-version 1.0.0
agvtool what-version
agvtool what-marketing-version
'''

import os
import sys
import argparse
import glob
import plistlib
from pbxproj import XcodeProject


NEW_VERSION = 'new-version'
NEW_MARKETING_VERSION = 'new-marketing-version'
WHAT_VERSION = 'what-version'
WHAT_MARKETING_VERSION = 'what-marketing-version'
SUPPORTED_COMMANDS = [WHAT_VERSION, WHAT_MARKETING_VERSION, NEW_VERSION, NEW_MARKETING_VERSION]

def __main__():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", help="supported commands: new-version")
    args, _ = parser.parse_known_args()

    if args.command not in SUPPORTED_COMMANDS:
        print("agvtool-port: Unsupported command")
        sys.exit(1)

    found_projects = glob.glob('*.xcodeproj')

    if len(found_projects) == 0:
        print("No project found at directory: {}".format(os.getcwd()))
        sys.exit(1)

    if len(found_projects) > 1:
        print("Found more than one project: {}".format(found_projects))
        sys.exit(1)

    project = XcodeProject.load('{}/project.pbxproj'.format(found_projects[0]))

    pbx_project = project.objects.get_objects_in_section('PBXProject')[0]
    first_target = project.get_object(pbx_project.targets[0])
    first_build_configuration_list = project.get_object(first_target.buildConfigurationList)
    first_build_configuration = project.get_object(first_build_configuration_list.buildConfigurations[0])
    first_infoplist_file = first_build_configuration.buildSettings['INFOPLIST_FILE']
    first_infoplist = plistlib.loads(open(first_infoplist_file, 'rb').read())
    build_configurations = []
    plist_paths = set()

    for target_id in pbx_project.targets:
        target = project.get_object(target_id)
        build_configuration_list = project.get_object(target.buildConfigurationList)
        for build_configuration_id in build_configuration_list.buildConfigurations:
            build_configuration = project.get_object(build_configuration_id)
            build_configurations.append(build_configuration)
            plist_path = build_configuration.buildSettings['INFOPLIST_FILE']
            plist_paths.add(plist_path)

    project_name = first_target.productName
    project_version = first_build_configuration.buildSettings['CURRENT_PROJECT_VERSION']
    project_marketing_version = first_infoplist['CFBundleShortVersionString']


    def write_plist_data(path, data):
        plist_file = open(path, 'rb')
        plist_data = plistlib.loads(plist_file.read())
        for key in data:
            plist_data[key] = data[key]
        plist_file.close()

        plist_file = open(path, 'wb')
        plist_file.write(plistlib.dumps(plist_data))
        plist_file.close()


    if args.command in [NEW_VERSION, NEW_MARKETING_VERSION]:
        parser.add_argument(
            "-all",
            help="The -all option will also update the CFBundleVersion Info.plist key.",
            action="store_true"
        )
        parser.add_argument("version", help="version number")
        args, _ = parser.parse_known_args()

        if args.command == NEW_VERSION:
            print('Setting version of project {} to:'.format(project_name))
            print('{}.'.format(args.version))

            for build_configuration in build_configurations:
                build_configuration.buildSettings['CURRENT_PROJECT_VERSION'] = args.version

            print('Also setting CFBundleVersion key (assuming it exists)')
            print('Updating CFBundleVersion in Info.plist(s)...')

            for plist_path in plist_paths:
                write_plist_data(plist_path, {'CFBundleVersion': args.version})
                print('Updated CFBundleVersion in "{}" to {}'.format(plist_path, args.version))

            print(os.getcwd())
            project.save()

        if args.command == NEW_MARKETING_VERSION:
            print('Setting CFBundleShortVersionString of project {} to:'.format(project_name))
            print('{}.'.format(args.version))
            print('Updating CFBundleShortVersionString in Info.plist(s)...')
            for plist_path in plist_paths:
                write_plist_data(plist_path, {'CFBundleShortVersionString': args.version})
                print('Updated CFBundleShortVersionString in "{}" to {}'.format(plist_path, args.version))

    if args.command == WHAT_VERSION:
        print("Current version of project {} is:\n    {}\n".format(project_name, project_version))

    if args.command == WHAT_MARKETING_VERSION:
        print("Current markerting version of project {} is:\n    {}\n".format(project_name, project_marketing_version))
