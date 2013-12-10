#!/usr/bin/python
#
# Directories Renamer
#
# Yauhen Yakimovich (c) 2013
#  - initial code outline
# Artur Yakimovich (c) 2013
#  - code finilizing
import os
import re
from os.path import join
import argparse
import threading
import sre_constants
from os import listdir, rmdir
import shutil

def dir_name_extract(metaxpress_name):
    # ^(?P<Plate>.*)_(?P<Well>[A-P][0-9]{2})_s(?P<Site>[0-9]*)
    #plate, well, site, channel
    pattern = re.compile(r"""^(?P<plate>.*)_                # plate and underscore
                             (?P<well>[A-P][0-9]{2})_       # well and underscore
                             s(?P<site>[0-9]*)_             # s site and underscore
                             w(?P<channel>[0-9]*)           # w channel
                             """, re.VERBOSE)
    match = pattern.match(metaxpress_name)

    plate = match.group("plate")
    well = match.group("well")
    site = match.group("site")
    channel = match.group("channel")
    
    return (plate, well, site, channel)


def move_to_parent_dir(folder_path):
    child_folder = 'TimePoint_1'
    for filename in listdir(join(folder_path, child_folder)):
        shutil.move(join(folder_path, child_folder, filename), join(folder_path, filename))
        rmdir(join(folder_path, child_folder))

def dir_rename(path_to_folders, filename_contains, test):
    '''
    Recursive RegExp Renamer
    '''
    countRenamedFiles = 0
    maxrecords = 0

    for root, dirs, files in os.walk(path_to_folders):
        for image_dirname in files:
            maxrecords = maxrecords + 1

    loopCounter = 0


    for root, dirs, files in os.walk(path_to_folders):
        for image_dirname in files:
            #image_filepath = join(root,image_dirname)
            #print image_filepath
            # print '%s file is in %s' % (image_dirname, image_filepath)
            # add string comparison to check if filename matches
            # our thumbnail criteria.
            isMatch = image_dirname.find(filename_contains)
            #isMatch = re.search(filename_contains, image_dirname)
            #print filename_contains
            #print isMatch.group(0)
            # Rename files matching the pattern.
            # print(isMatch)
            if isMatch != -1:
                (plate, well, site, channel) = dir_name_extract(image_dirname)
                #print (plate, well, site, channel)
                #bNW-002-1_wP24_s9_z1_t1_cGFP_u001.tif
                if channel == '1':
                    renamed_dir_name = 'b%s_w%s_s%s_z1_t1_cDAPI_u001.tif' % (plate, well, site)
                elif channel == '2':
                    renamed_dir_name = 'b%s_w%s_s%s_z1_t1_cGFP_u001.tif' % (plate, well, site)
                else:
                    print 'error: no channel detected in file %s' % join(root,image_dirname)
                    exit()
                
                if test == 0:
                    os.rename(join(root,image_dirname), join(root,renamed_dir_name))
                    print '%s -- renamed\n into %s \n\n ' % (join(root,image_dirname), renamed_dir_name)
                elif test == 1:
                    print '%s would be renamed\n into %s in a non-test mode\n\n ' % (image_dirname, renamed_dir_name)
                
                countRenamedFiles = countRenamedFiles + 1
            # if isMatch == -1:
            # print '%s file is NOT a thumbnail and will not be removed ' % (image_dirname)
            loopCounter = loopCounter + 1
            # print '%s out of %s complete ' % (loopCounter, maxrecords)
            # for i in range(50+1):

            # make a progress bar
            i = int(round(float(loopCounter)/float(maxrecords) * 50, 0))
            threading._sleep(0.05)
            i2 = i * 2
            print "\r%3d percent complete" % i2, ('*'*i)+('-'*(50-i))

            # print '\n %s percent completed... ' % (round(loopCounter/maxrecords, 2) * 100)
    if test == 0:
        print '%s Images files successfully renamed. Have a nice day!' % (countRenamedFiles)
    elif test == 1:
        print '%s Images files would have been renamed in a non-test mode. Have a nice day!' % (countRenamedFiles)
# Main
if __name__ == '__main__':
# uncomment for run in command line

    parser = argparse.ArgumentParser('Regexp Renamer')
    parser.add_argument('--path', default='None', 
                        help='Folder with images')
    parser.add_argument('--name_contains',default='None',
                        help='name_contains for images')
    parser.add_argument('--test',default=1,
                        help='test will only show how it would rename images for safety, to actually rename images use --test 0')
    args = parser.parse_args()
    # here path is now an optional argument, if none user will be prompted to enter a new one
    print('\n\n=========== Welcome to Instant MetaXpress Directories Renamer ===================')
    print('Artur Yakimovich & Yauhen Yakimovich (c) 2013. University of Zurich. IMLS. v1.0')
    print('===============================================================================\n\n')

    # args.path.print_help()

    # Check whether path and name_contains are correct and prompt the user to enter a new one if not
    ArgsNotCorrect = True
    while ArgsNotCorrect:
        if not args.path or not os.path.exists(args.path):
            print 'Warning, path not found or not entered "%s"!\n' % args.path
            args.path = raw_input('\nEnter the path to a folder where you want to recursively rename: ')
            print 'You have entered: "%s". Proceeding...' % args.path
        elif not args.name_contains:            
            print 'Warning, path not found or not entered "%s"!\n' % args.path
            args.name_contains = raw_input('\nEnter the name_contains: ')
            print 'You have entered: "%s". Proceeding...' % args.name_contains
        else:
            ArgsNotCorrect = False
            print 'arguments parsed correctly\n\n '

    # Let check if name_contains works.
    try:
        regexp = re.compile(args.name_contains)
    except sre_constants.error as exception:
        print type(exception)
    #exit()
    # At this point we know that path argument must exist.
    dir_rename(args.path, args.name_contains, float(args.test))
