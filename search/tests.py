################################################################################
# 
# Human Variome Database Portal.
#
# === License ===
#
# Last Author:   $Author: MelvinLuong $
# Last Revision: $Rev: 302 $
# Last Modified: $Date: 2011-03-18 16:19:12 +1100 (Fri, 18 Mar 2011) $ 
#
# === Description ===
#
#
################################################################################



"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""
from parser import variant_parser
from views.variant import ConvertSymbolsToUrlFriendly, ConvertToSymbols
from django.test import TestCase

class SearchTest(TestCase):
    def testParser(self):
        variant = 'c.123c>t'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','123','','','','','','c>t','sub',''],
                             'Failed with: ' + variant)
        
        variant = 'c.123_456c>t'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','','','123','','456','','c>t','sub',''],
                             'Failed with: ' + variant)
        
        variant = 'c.123+23c>t'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','123',23,'','','','','c>t','sub',''],
                             'Failed with: ' + variant)
        
        variant = 'c.123-23c>t'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','123',-23,'','','','','c>t','sub',''],
                             'Failed with: ' + variant)

        variant = 'c.-123-23c>t'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','-123',-23,'','','','','c>t','sub',''],
                             'Failed with: ' + variant)
        
        variant = 'c.123+23_456c>t'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','','','123',23,'456','','c>t','sub',''],
                             'Failed with: ' + variant)

        variant = 'c.-123+23c>t'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','-123',23,'','','','','c>t','sub',''],
                             'Failed with: ' + variant)
        
        variant = 'c.123-23_456c>t'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','','','123',-23,'456','','c>t','sub',''],
                             'Failed with: ' + variant)
        
        variant = 'c.123_456+56c>t'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','','','123','','456',56,'c>t','sub',''],
                             'Failed with: ' + variant)
        
        variant = 'c.123_456-56c>t'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','','','123','','456',-56,'c>t','sub',''],
                             'Failed with: ' + variant)        
        
        variant = 'c.123+23_456+56c>t'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','','','123',23,'456',56,'c>t','sub',''],
                             'Failed with: ' + variant)
        
        variant = 'c.123-23_456-56c>t'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','','','123',-23,'456',-56,'c>t','sub',''],
                             'Failed with: ' + variant)
        
        variant = 'c.123+23_456-56c>t'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','','','123',23,'456',-56,'c>t','sub',''],
                             'Failed with: ' + variant)
        
        variant = 'c.123-23_456+56c>t'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','','','123',-23,'456',56,'c>t','sub',''],
                             'Failed with: ' + variant)

        variant = 'c.123-?'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','123','-?','','','','','','',''],
                             'Failed with: ' + variant)

        variant = 'c.123+?'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','123','+?','','','','','','',''],
                             'Failed with: ' + variant)

        variant = 'c.123-?c>t'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','123','-?','','','','','c>t','sub',''],
                             'Failed with: ' + variant)

        variant = 'c.123+?c>t'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','123','+?','','','','','c>t','sub',''],
                             'Failed with: ' + variant)

        variant = 'c.123-?_456'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','','','123','-?','456','','','',''],
                             'Failed with: ' + variant)

        variant = 'c.123+?_456'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','','','123','+?','456','','','',''],
                             'Failed with: ' + variant)

        variant = 'c.123_456-?'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','','','123','','456','-?','','',''],
                             'Failed with: ' + variant)
                             
        variant = 'c.123_456+?'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','','','123','','456','+?','','',''],
                             'Failed with: ' + variant)

        variant = 'c.123-?_456c>t'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','','','123','-?','456','','c>t','sub',''],
                             'Failed with: ' + variant)

        variant = 'c.123+?_456c>t'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','','','123','+?','456','','c>t','sub',''],
                             'Failed with: ' + variant)

        variant = 'c.123_456-?c>t'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','','','123','','456','-?','c>t','sub',''],
                             'Failed with: ' + variant)

        variant = 'c.123_456+?c>t'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','','','123','','456','+?','c>t','sub',''],
                             'Failed with: ' + variant)
        
        variant = 'c.123-45_456-?'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','','','123',-45,'456','-?','','',''],
                             'Failed with: ' + variant)

        variant = 'c.123-45_456+?'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','','','123',-45,'456','+?','','',''],
                             'Failed with: ' + variant)

        variant = 'c.123-45_456-?'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','','','123',-45,'456','-?','','',''],
                             'Failed with: ' + variant)

        variant = 'c.123-?_456+78'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','','','123','-?','456',78,'','',''],
                             'Failed with: ' + variant)

        variant = 'c.123+?_456-78'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','','','123','+?','456',-78,'','',''],
                             'Failed with: ' + variant)

        variant = 'c.123-45_456-?c>t'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','','','123',-45,'456','-?','c>t','sub',''],
                             'Failed with: ' + variant)

        variant = 'c.123-45_456+?c>t'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','','','123',-45,'456','+?','c>t','sub',''],
                             'Failed with: ' + variant)

        variant = 'c.123-45_456-?c>t'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','','','123',-45,'456','-?','c>t','sub',''],
                             'Failed with: ' + variant)

        variant = 'c.123-?_456+78c>t'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','','','123','-?','456',78,'c>t','sub',''],
                             'Failed with: ' + variant)

        variant = 'c.123+?_456-78c>t'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','','','123','+?','456',-78,'c>t','sub',''],
                             'Failed with: ' + variant)

        variant = 'c.123del'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','123','','','','','','del','del',''],
                             'Failed with: ' + variant)

        variant = 'c.123delTAC'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','123','','','','','','del','del','TAC'],
                             'Failed with: ' + variant)

        variant = 'c.123del52'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','123','','','','','','del','del','52'],
                             'Failed with: ' + variant)

        variant = 'c.123dup'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','123','','','','','','dup','dup',''],
                             'Failed with: ' + variant)

        variant = 'c.123dupTAC'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','123','','','','','','dup','dup','TAC'],
                             'Failed with: ' + variant)

        variant = 'c.123dup52'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','123','','','','','','dup','dup','52'],
                             'Failed with: ' + variant)

        variant = 'c.123inv'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','123','','','','','','inv','inv',''],
                             'Failed with: ' + variant)

        variant = 'c.123invTAC'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','123','','','','','','inv','inv','TAC'],
                             'Failed with: ' + variant)

        variant = 'c.123inv52'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','123','','','','','','inv','inv','52'],
                             'Failed with: ' + variant)

        variant = 'c.-123c>t'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','-123','','','','','','c>t','sub',''],
                             'Failed with: ' + variant)

        variant = 'c.-123_456c>t'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','','','-123','','456','','c>t','sub',''],
                             'Failed with: ' + variant)
        
        variant = 'c.-123+23_456c>t'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','','','-123',23,'456','','c>t','sub',''],
                             'Failed with: ' + variant)

        variant = 'c.-123_456+56c>t'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','','','-123','','456',56,'c>t','sub',''],
                             'Failed with: ' + variant)

        variant = 'c.-123_456-56c>t'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','','','-123','','456',-56,'c>t','sub',''],
                             'Failed with: ' + variant)
        
        variant = 'c.-123+23_456+56c>t'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','','','-123',23,'456',56,'c>t','sub',''],
                             'Failed with: ' + variant)
        
        variant = 'c.-123-23_456-56c>t'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','','','-123',-23,'456',-56,'c>t','sub',''],
                             'Failed with: ' + variant)
        
        variant = 'c.-123+23_456-56c>t'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','','','-123',23,'456',-56,'c>t','sub',''],
                             'Failed with: ' + variant)
        
        variant = 'c.-123-23_456+56c>t'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','','','-123',-23,'456',56,'c>t','sub',''],
                             'Failed with: ' + variant)

        variant = 'c.-123-?'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','-123','-?','','','','','','',''],
                             'Failed with: ' + variant)

        variant = 'c.-123+?'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','-123','+?','','','','','','',''],
                             'Failed with: ' + variant)

        variant = 'c.-123-?c>t'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','-123','-?','','','','','c>t','sub',''],
                             'Failed with: ' + variant)

        variant = 'c.-123+?c>t'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','-123','+?','','','','','c>t','sub',''],
                             'Failed with: ' + variant)

        variant = 'c.-123-?_456'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','','','-123','-?','456','','','',''],
                             'Failed with: ' + variant)

        variant = 'c.-123+?_456'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','','','-123','+?','456','','','',''],
                             'Failed with: ' + variant)

        variant = 'c.-123_456-?'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','','','-123','','456','-?','','',''],
                             'Failed with: ' + variant)
                             
        variant = 'c.-123_456+?'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','','','-123','','456','+?','','',''],
                             'Failed with: ' + variant)

        variant = 'c.-123-?_456c>t'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','','','-123','-?','456','','c>t','sub',''],
                             'Failed with: ' + variant)

        variant = 'c.-123+?_456c>t'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','','','-123','+?','456','','c>t','sub',''],
                             'Failed with: ' + variant)

        variant = 'c.-123_456-?c>t'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','','','-123','','456','-?','c>t','sub',''],
                             'Failed with: ' + variant)

        variant = 'c.-123_456+?c>t'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','','','-123','','456','+?','c>t','sub',''],
                             'Failed with: ' + variant)
        
        variant = 'c.-123-45_456-?'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','','','-123',-45,'456','-?','','',''],
                             'Failed with: ' + variant)

        variant = 'c.-123-45_456+?'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','','','-123',-45,'456','+?','','',''],
                             'Failed with: ' + variant)

        variant = 'c.-123-45_456-?'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','','','-123',-45,'456','-?','','',''],
                             'Failed with: ' + variant)

        variant = 'c.-123-?_456+78'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','','','-123','-?','456',78,'','',''],
                             'Failed with: ' + variant)

        variant = 'c.-123+?_456-78'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','','','-123','+?','456',-78,'','',''],
                             'Failed with: ' + variant)

        variant = 'c.-123-45_456-?c>t'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','','','-123',-45,'456','-?','c>t','sub',''],
                             'Failed with: ' + variant)

        variant = 'c.-123-45_456+?c>t'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','','','-123',-45,'456','+?','c>t','sub',''],
                             'Failed with: ' + variant)

        variant = 'c.-123-45_456-?c>t'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','','','-123',-45,'456','-?','c>t','sub',''],
                             'Failed with: ' + variant)

        variant = 'c.-123-?_456+78c>t'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','','','-123','-?','456',78,'c>t','sub',''],
                             'Failed with: ' + variant)

        variant = 'c.-123+?_456-78c>t'
        self.failUnlessEqual(variant_parser.parse(variant),
                             ['c','','','-123','+?','456',-78,'c>t','sub',''],
                             'Failed with: ' + variant)

        
    def testValidator(self):
        # valid variants strings
        variants = ['c.123c>t','c.123','c.123_456c>t','c.123_456','c.123-23c>t','c.123-23','c.123+23c>t','c.123+23',
                    'c.123-23_456c>t','c.123-23_456','c.123_456+56c>t','c.123_456+56','c.123_456-56c>t','c.123_456-56',
                    'c.123+23_456+56c>t','c.123+23_456+56','c.123-23_456-56c>t','c.123-23_456-56','c.123+23_456-56c>t',
                    'c.123+23_456-56','c.123-23_456+56c>t','c.123-23_456+56',
                    'c.-123c>t','c.-123','c.-123_456c>t','c.-123_456','c.-123-23c>t','c.-123-23','c.-123+23c>t','c.-123+23',
                    'c.-123-23_456c>t','c.-123-23_456','c.-123_456+56c>t','c.-123_456+56','c.-123_456-56c>t','c.-123_456-56',
                    'c.-123+23_456+56c>t','c.-123+23_456+56','c.-123-23_456-56c>t','c.-123-23_456-56','c.-123+23_456-56c>t',
                    'c.-123+23_456-56','c.-123-23_456+56c>t','c.-123-23_456+56'
                    ]
        
        for variant in variants:
            self.failUnlessEqual(variant_parser.variant_validation(variant), True, 'Failed with ' + variant)
        
        # invalid variant strings
        variants = ['c.123_','c.123+','c.123-','c.123_456_','c.123_456-','c.123_456+','c.123-23_','c.123-23+','c.123-23-',
                    'c.123+23_','c.123+23+','c.123+23-','c.123-23_456_','c.123-23_456+','c.123-23_456-','c.123+23_456_',
                    'c.123+23_456+','c.123+23_456-','c.123+23_456+56_','c.123+23_456+56-','c.123+23_456+56+',
                    'c.123-23_456-56_','c.123-23_456-56+','c.123-23_456-56-','c.123+23_456-56_','c.123+23_456-56+',
                    'c.123-23_456+56_','c.123-23_456+56+','c.123-23_456+56-']
        
        for variant in variants:
            self.failUnlessEqual(variant_parser.variant_validation(variant), False, 'Failed with ' + variant)
            
    
    def testConvertSymbolsToUrlFriendly(self):
        variant = 'c.123c>t'
        self.failUnlessEqual(ConvertSymbolsToUrlFriendly(variant), 'c.123c.gt.t', 'Failed with ' + variant)
        
        variant = 'c.123_456c>t'
        self.failUnlessEqual(ConvertSymbolsToUrlFriendly(variant), 'c.123.us.456c.gt.t', 'Failed with ' + variant)
        
        variant = 'c.123+23c>t'
        self.failUnlessEqual(ConvertSymbolsToUrlFriendly(variant), 'c.123+23c.gt.t', 'Failed with ' + variant)
        
        variant = 'c.123-23c>t'
        self.failUnlessEqual(ConvertSymbolsToUrlFriendly(variant), 'c.123-23c.gt.t', 'Failed with ' + variant)
        
        variant = 'c.123+23_456c>t'
        self.failUnlessEqual(ConvertSymbolsToUrlFriendly(variant), 'c.123+23.us.456c.gt.t', 'Failed with ' + variant)
        
        variant = 'c.123-23_456c>t'
        self.failUnlessEqual(ConvertSymbolsToUrlFriendly(variant), 'c.123-23.us.456c.gt.t', 'Failed with ' + variant)
        
        variant = 'c.123_456+56c>t'
        self.failUnlessEqual(ConvertSymbolsToUrlFriendly(variant), 'c.123.us.456+56c.gt.t', 'Failed with ' + variant)
        
        variant = 'c.123_456-56c>t'
        self.failUnlessEqual(ConvertSymbolsToUrlFriendly(variant), 'c.123.us.456-56c.gt.t', 'Failed with ' + variant)
        
        variant = 'c.123+23_456+56c>t'
        self.failUnlessEqual(ConvertSymbolsToUrlFriendly(variant), 'c.123+23.us.456+56c.gt.t', 'Failed with ' + variant)
        
        variant = 'c.123-23_456-56c>t'
        self.failUnlessEqual(ConvertSymbolsToUrlFriendly(variant), 'c.123-23.us.456-56c.gt.t', 'Failed with ' + variant)
        
        variant = 'c.123+23_456-56c>t'
        self.failUnlessEqual(ConvertSymbolsToUrlFriendly(variant), 'c.123+23.us.456-56c.gt.t', 'Failed with ' + variant)
        
        variant = 'c.123-23_456+56c>t'
        self.failUnlessEqual(ConvertSymbolsToUrlFriendly(variant), 'c.123-23.us.456+56c.gt.t', 'Failed with ' + variant)
        
    def testConvertToSymbols(self):
        variant = 'c.123c.gt.t'
        self.failUnlessEqual(ConvertToSymbols(variant), 'c.123c>t', 'Failed with ' + variant)
        
        variant = 'c.123.us.456c.gt.t'
        self.failUnlessEqual(ConvertToSymbols(variant), 'c.123_456c>t', 'Failed with ' + variant)
        
        variant = 'c.123+23c.gt.t'
        self.failUnlessEqual(ConvertToSymbols(variant), 'c.123+23c>t', 'Failed with ' + variant)
        
        variant = 'c.123-23c.gt.t'
        self.failUnlessEqual(ConvertToSymbols(variant), 'c.123-23c>t', 'Failed with ' + variant)
        
        variant = 'c.123+23.us.456c.gt.t'
        self.failUnlessEqual(ConvertToSymbols(variant), 'c.123+23_456c>t', 'Failed with ' + variant)
        
        variant = 'c.123-23.us.456c.gt.t'
        self.failUnlessEqual(ConvertToSymbols(variant), 'c.123-23_456c>t', 'Failed with ' + variant)
        
        variant = 'c.123.us.456+56c.gt.t'
        self.failUnlessEqual(ConvertToSymbols(variant), 'c.123_456+56c>t', 'Failed with ' + variant)
        
        variant = 'c.123.us.456-56c.gt.t'
        self.failUnlessEqual(ConvertToSymbols(variant), 'c.123_456-56c>t', 'Failed with ' + variant)
        
        variant = 'c.123+23.us.456+56c.gt.t'
        self.failUnlessEqual(ConvertToSymbols(variant), 'c.123+23_456+56c>t', 'Failed with ' + variant)
        
        variant = 'c.123-23.us.456-56c.gt.t'
        self.failUnlessEqual(ConvertToSymbols(variant), 'c.123-23_456-56c>t', 'Failed with ' + variant)
        
        variant = 'c.123+23.us.456-56c.gt.t'
        self.failUnlessEqual(ConvertToSymbols(variant), 'c.123+23_456-56c>t', 'Failed with ' + variant)
        
        variant = 'c.123-23.us.456+56c.gt.t'
        self.failUnlessEqual(ConvertToSymbols(variant), 'c.123-23_456+56c>t', 'Failed with ' + variant)
