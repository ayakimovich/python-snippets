#!/usr/bin/python
#
# Instant MetaXpress Thumbnail Remover
# v1.1
# Yauhen Yakimovich (c) 2011
#  - initial code outline
# Artur Yakimovich (c) 2011
#  - code finilizing
import os
from os.path import join, getsize
import argparse
import sys
import threading


def purge_thumbs(path_to_images,name_pattern):
    '''
    Recursive thumbnails removal.
     path_to_images - looks inside subfolders of this path.
    '''
    countDeletedFiles = 0
    maxrecords = 0

    for root, dirs, files in os.walk(path_to_images):
        for image_filename in files:
            maxrecords = maxrecords + 1

    loopCounter = 0


    for root, dirs, files in os.walk(path_to_images):
        for image_filename in files:
            image_filepath = join(root,image_filename)
#            print '%s file is in %s' % (image_filename, image_filepath)
            # add string comparison to check if filename matches
            # our thumbnail criteria.
            isMatch = image_filename.find(name_pattern)

            # remove thumbnail once found.
#            print(isMatch)
            if isMatch != -1:
                print '%s -- removed\n\n ' % (image_filename)
                os.remove(image_filepath)
                countDeletedFiles = countDeletedFiles + 1
#            if isMatch == -1:
#                print '%s file is NOT a thumbnail and will not be removed ' % (image_filename)
            loopCounter = loopCounter + 1
 #           print '%s out of %s complete ' % (loopCounter, maxrecords)
 #           for i in range(50+1):

# make a progress bar
            i = int(round(float(loopCounter)/float(maxrecords) * 50, 0))
            threading._sleep(0.05)
            i2 = i * 2
            print "\r%3d percent complete" % i2, ('*'*i)+('-'*(50-i))

#            print '\n %s percent completed... ' % (round(loopCounter/maxrecords, 2) * 100)

    print '%s Thumbnail files successfully removed. Have a nice day!' % (countDeletedFiles)

# Main
if __name__ == '__main__':
# uncomment for run in command line

   parser = argparse.ArgumentParser('Thumbnails cleaner')
   parser.add_argument('-path')
   parser.add_argument('-pattern')
   args = parser.parse_args()
# here path is now an optional argument, if none user will be prompted to enter a new one
   print ('\n\n=========== Welcome to Instant MetaXpress Thumbnail Remover ===================')
   print ('Artur Yakimovich & Yauhen Yakimovich (c) 2011. University of Zurich. IMLS. v1.1')
   print ('===============================================================================\n\n')

 #   args.path.print_help()
# Check whether path is correct and prmpt the user to enter a new one if not
   pathNotCorrect = True
   while pathNotCorrect:
        if not args.path or not os.path.exists(args.path):
             print 'Warning, path not found or not entered "%s"!\n' % args.path
#            args.path.print_help()
             args.path = raw_input('\nEnter the path to a folder where you want to recursively remove thumbnails: ')
             print 'You have entered: "%s". Proceeding...' % args.path
#	    if not args.pattern or not os.pattern.exists(args.pattern):
#             print 'Warning, path not found or not entered "%s"!\n' % args.pattern
#            args.path.print_help()
#             args.pattern = raw_input('\nEnter the path to a folder where you want to recursively remove thumbnails: ')
#             print 'You have entered: "%s". Proceeding...' % args.pattern
#            exit()
        else:
             pathNotCorrect = False
    # At this point we know that path argument must exist.
   purge_thumbs(args.path, args.pattern)