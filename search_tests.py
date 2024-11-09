from search import search, article_length, unique_authors, most_recent_article, favorite_author, title_and_author, refine_search, display_result
from search_tests_helper import get_print, print_basic, print_advanced, print_advanced_option
from wiki import article_metadata
from unittest.mock import patch
from unittest import TestCase, main

class TestSearch(TestCase):

    ##############
    # UNIT TESTS #
    ##############

    def test_example_unit_test(self):
        expected_search_soccer_results = [
            ['Spain national beach soccer team', 'jack johnson', 1233458894, 1526],
            ['Will Johnson (soccer)', 'Burna Boy', 1218489712, 3562],
            ['Steven Cohen (soccer)', 'Mack Johnson', 1237669593, 2117]
        ]
        self.assertEqual(search('soccer'), expected_search_soccer_results)

    
    def test_search(self):
        expected_empty_search_results = []
        self.assertEqual(search(''), expected_empty_search_results)

        expected_kathmandu_search_results = []
        self.assertEqual(search('kathmandu'), expected_kathmandu_search_results)

        expected_fisk_search_results = [['Fisk University', 'RussBot', 1263393671, 16246]]
        self.assertEqual(search('fisk'), expected_fisk_search_results)

        expected_fisk_case_insensitive_search_results = [['Fisk University', 'RussBot', 1263393671, 16246]]
        self.assertEqual(search('FISK'), expected_fisk_search_results)

        expected_computer_search_results = [['Ken Kennedy (computer scientist)', 'Mack Johnson', 1246308670, 4144], ['Human computer', 'Bearcat', 1248275178, 4750], ['List of dystopian music, TV programs, and games', 'Bearcat', 1165317338, 13458], ['Single-board computer', 'Gary King', 1220260601, 8271], ['Personal computer', 'Pegship', 1220391790, 45663], ['Digital photography', 'Mr Jake', 1095727840, 18093], ['Mode (computer interface)', 'Pegship', 1182732608, 2991]]
        self.assertEqual(search('computer'), expected_computer_search_results)
    
    def test_most_recent_articles(self):

        expected_fisk_recent_result = ['Fisk University', 'RussBot', 1263393671, 16246]
        metadata = search('fisk')
        self.assertEqual(most_recent_article(metadata), expected_fisk_recent_result)

        expected_music_recent_result = ['Rock music', 'Mack Johnson', 1258069053, 119498]
        metadata = search('MuSic')
        self.assertEqual(most_recent_article(metadata), expected_music_recent_result)

        expected_no_article= ''
        metadata = search('navy blue')
        self.assertEqual(most_recent_article(metadata), expected_no_article)

        metadata = search('')
        self.assertEqual(most_recent_article(metadata), '')

    def test_favorite_author(self):
        
        metadata = search('soccer')
        self.assertEqual(favorite_author('Jack Johnson', metadata), True)
        
        metadata = search('man')
        self.assertEqual(favorite_author('Jack', metadata), False)

        metadata = search('boy')
        self.assertEqual(favorite_author('fisk', metadata), False)

        metadata = search("")
        self.assertEqual(favorite_author('fisk', metadata), False)

        metadata = search("")
        self.assertEqual(favorite_author('', metadata), False)

    def test_title_and_author(self):

        metadata = search("fisk")
        expected_fisk_result = [('Fisk University', 'RussBot')]
        self.assertEqual(title_and_author(metadata),expected_fisk_result )

        metadata = search("")
        expected_nep_result = []
        self.assertEqual(title_and_author(metadata),expected_nep_result )

        metadata = search("FiSk")
        expected_FiSk_result = [('Fisk University', 'RussBot')]
        self.assertEqual(title_and_author(metadata),expected_FiSk_result )

        metadata = search("Boy")
        expected_boy_result = []
        self.assertEqual(title_and_author(metadata),expected_boy_result )
    

    def test_article_length(self):
        expected_search_thandiram_3k_results = []
        self.assertEqual(article_length(3000, search('thandiram')), expected_search_thandiram_3k_results)

        expected_search_soccer_0_results = []
        self.assertEqual(article_length(0, search('soccer')), expected_search_soccer_0_results)

        expected_search_fisk_100_results = []
        self.assertEqual(article_length(100, search('fisk')), expected_search_fisk_100_results)

        expected_search_this_1000_results = [['Lua (programming language)', 'Burna Boy', 1113957128, 0], ['The Hunchback of Notre Dame (musical)', 'Nihonjoe', 1192176615, 42]]
        self.assertEqual(article_length(1000, search('this')), expected_search_this_1000_results)

    def test_unique_authors(self):
        expected_authors_3_the_results = [['List of Canadian musicians', 'Jack Johnson', 1181623340, 21023], ['French pop music', 'Mack Johnson', 1172208041, 5569], ['1922 in music', 'Gary King', 1242717698, 11576]]
        self.assertEqual(unique_authors(3, search('the')), expected_authors_3_the_results)

        expected_authors_0_eye_results = []
        self.assertEqual(unique_authors(0, search('eye')), expected_authors_0_eye_results)

        expected_no_author = []
        self.assertEqual(unique_authors(3, search('thandiram')), expected_no_author)

        expected_authors_100_eye_results = [['Kevin Cadogan', 'Mr Jake', 1144136316, 3917]]
        self.assertEqual(unique_authors(100, search('eye')), expected_authors_100_eye_results)
    
    def test_refine_search(self):
        expected_intersection = [['Will Johnson (soccer)', 'Burna Boy', 1218489712, 3562], ['Steven Cohen (soccer)', 'Mack Johnson', 1237669593, 2117]]
        metadata_soccer = search('soccer')
        self.assertEqual(refine_search('his', metadata_soccer), expected_intersection)

        expected_intersection2 = [['Will Johnson (soccer)', 'Burna Boy', 1218489712, 3562]]
        self.assertEqual(refine_search('team', metadata_soccer), expected_intersection2)

        expected_no_intersection = []
        metadata_fisk = search('fisk')
        self.assertEqual(refine_search('his', metadata_fisk), expected_no_intersection)

        expected_both_empty = []
        metadata_both_empty = []
        self.assertEqual(refine_search('thandiram', metadata_both_empty), expected_both_empty)

        expected_single_empty = []
        metadata_single_empty = []
        self.assertEqual(refine_search('his', metadata_single_empty), expected_single_empty)

        

    #####################
    # INTEGRATION TESTS #
    #####################

    @patch('builtins.input')
    def test_example_integration_test(self, input_mock):
        keyword = 'soccer'
        advanced_option = 1
        advanced_response = 3000

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: [['Spain national beach soccer team', 'jack johnson', 1233458894, 1526], ['Steven Cohen (soccer)', 'Mack Johnson', 1237669593, 2117]]\n"

        self.assertEqual(output, expected)


    @patch('builtins.input')
    def test_fisk_basic_search(self, input_mock):
        keyword = 'fisk'
        advanced_option = 7

        output = get_print(input_mock, [keyword, advanced_option])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + "\nHere are your articles: [['Fisk University', 'RussBot', 1263393671, 16246]]\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_empty_basic_search(self, input_mock):
        keyword = ''
        advanced_option = 7

        output = get_print(input_mock, [keyword, advanced_option])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + "\nNo articles found\n"

        self.assertEqual(output, expected)


    @patch('builtins.input')
    def test_basic_keyword_not_found(self, input_mock):
        keyword = 'meharry'
        advanced_option = 7

        output = get_print(input_mock, [keyword, advanced_option])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + "\nNo articles found\n"

        self.assertEqual(output, expected)
    
    @patch('builtins.input')
    def test_article_length_100(self, input_mock):
        keyword = 'computer'
        advanced_option = 1
        advanced_response = 100

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nNo articles found\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_article_length_2000(self, input_mock):
        keyword = 'computer'
        advanced_option = 1
        advanced_response = 6000

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: [['Ken Kennedy (computer scientist)', 'Mack Johnson', 1246308670, 4144], ['Human computer', 'Bearcat', 1248275178, 4750], ['Mode (computer interface)', 'Pegship', 1182732608, 2991]]\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_article_length_no_article(self, input_mock):
        keyword = ''
        advanced_option = 1
        advanced_response = 10000

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nNo articles found\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_article_length_0(self, input_mock):
        keyword = 'simara'
        advanced_option = 1
        advanced_response = 0

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nNo articles found\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_unique_authors_3(self, input_mock):
        keyword = 'computer'
        advanced_option = 2
        advanced_response = 3

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: [['Ken Kennedy (computer scientist)', 'Mack Johnson', 1246308670, 4144], ['Human computer', 'Bearcat', 1248275178, 4750], ['Single-board computer', 'Gary King', 1220260601, 8271]]\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_unique_authors_more_than_max(self, input_mock):
        keyword = 'computer'
        advanced_option = 2
        advanced_response = 100

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: [['Ken Kennedy (computer scientist)', 'Mack Johnson', 1246308670, 4144], ['Human computer', 'Bearcat', 1248275178, 4750], ['Single-board computer', 'Gary King', 1220260601, 8271], ['Personal computer', 'Pegship', 1220391790, 45663], ['Digital photography', 'Mr Jake', 1095727840, 18093]]\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_unique_authors_0(self, input_mock):
        keyword = 'computer'
        advanced_option = 2
        advanced_response = 0

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nNo articles found\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_unique_authors_no_article(self, input_mock):
        keyword = 'bandipur'
        advanced_option = 2
        advanced_response = 20

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nNo articles found\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_most_recent_article_computer(self, input_mock):
        keyword = 'computer'
        advanced_option = 3


        output = get_print(input_mock, [keyword, advanced_option])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option)  + "\nHere are your articles: ['Human computer', 'Bearcat', 1248275178, 4750]\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_most_recent_article_no_article(self, input_mock):
        keyword = 'bara'
        advanced_option = 3


        output = get_print(input_mock, [keyword, advanced_option])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option)  + "\nNo articles found\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_most_recent_article_fisk(self, input_mock):
        keyword = 'fisk'
        advanced_option = 3


        output = get_print(input_mock, [keyword, advanced_option])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option)  + "\nHere are your articles: ['Fisk University', 'RussBot', 1263393671, 16246]\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_favorite_author_exist(self, input_mock):
        keyword = 'computer'
        advanced_option = 4
        advanced_response = 'Bearcat'

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: [['Ken Kennedy (computer scientist)', 'Mack Johnson', 1246308670, 4144], ['Human computer', 'Bearcat', 1248275178, 4750], ['List of dystopian music, TV programs, and games', 'Bearcat', 1165317338, 13458], ['Single-board computer', 'Gary King', 1220260601, 8271], ['Personal computer', 'Pegship', 1220391790, 45663], ['Digital photography', 'Mr Jake', 1095727840, 18093], ['Mode (computer interface)', 'Pegship', 1182732608, 2991]]\nYour favorite author is in the returned articles!\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_favorite_author_not_exist(self, input_mock):
        keyword = 'computer'
        advanced_option = 4
        advanced_response = 'manoj bagale'

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: [['Ken Kennedy (computer scientist)', 'Mack Johnson', 1246308670, 4144], ['Human computer', 'Bearcat', 1248275178, 4750], ['List of dystopian music, TV programs, and games', 'Bearcat', 1165317338, 13458], ['Single-board computer', 'Gary King', 1220260601, 8271], ['Personal computer', 'Pegship', 1220391790, 45663], ['Digital photography', 'Mr Jake', 1095727840, 18093], ['Mode (computer interface)', 'Pegship', 1182732608, 2991]]\nYour favorite author is not in the returned articles!\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_favorite_author_no_article(self, input_mock):
        keyword = 'khadagpur'
        advanced_option = 4
        advanced_response = 'manoj bagale'

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nNo articles found\nYour favorite author is not in the returned articles!\n"

        self.assertEqual(output, expected)
        

    @patch('builtins.input')
    def test_title_and_author_computer(self, input_mock):
        keyword = 'computer'
        advanced_option = 5

        output = get_print(input_mock, [keyword, advanced_option])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + "\nHere are your articles: [('Ken Kennedy (computer scientist)', 'Mack Johnson'), ('Human computer', 'Bearcat'), ('List of dystopian music, TV programs, and games', 'Bearcat'), ('Single-board computer', 'Gary King'), ('Personal computer', 'Pegship'), ('Digital photography', 'Mr Jake'), ('Mode (computer interface)', 'Pegship')]\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_title_and_author_empty(self, input_mock):
        keyword = ''
        advanced_option = 5

        output = get_print(input_mock, [keyword, advanced_option])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + "\nNo articles found\n"

    @patch('builtins.input')
    def test_title_and_author_no_article(self, input_mock):
        keyword = 'Wadakam'
        advanced_option = 5

        output = get_print(input_mock, [keyword, advanced_option])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + "\nNo articles found\n"

        self.assertEqual(output, expected)


    @patch('builtins.input')
    def test_refine_search_intersetion(self, input_mock):
        keyword1 = 'his'
        keyword2 = 'book'
        advanced_option = 6

        output = get_print(input_mock, [keyword1, advanced_option, keyword2])
        expected = print_basic() + keyword1 + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + keyword2 + "\n\nHere are your articles: [['List of dystopian music, TV programs, and games', 'Bearcat', 1165317338, 13458], ['Annie (musical)', 'Jack Johnson', 1223619626, 27558]]\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_refine_search_no_intersetion(self, input_mock):
        keyword1 = 'fisk'
        keyword2 = 'computer'
        advanced_option = 6

        output = get_print(input_mock, [keyword1, advanced_option, keyword2])
        expected = print_basic() + keyword1 + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + keyword2 + "\n\nNo articles found\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_refine_search_no_intersetion_no_articles(self, input_mock):
        keyword1 = 'rajaram'
        keyword2 = 'thandiram'
        advanced_option = 6

        output = get_print(input_mock, [keyword1, advanced_option, keyword2])
        expected = print_basic() + keyword1 + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + keyword2 + "\n\nNo articles found\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_refine_search_empty_keywords(self, input_mock):
        keyword1 = ''
        keyword2 = ''
        advanced_option = 6

        output = get_print(input_mock, [keyword1, advanced_option, keyword2])
        expected = print_basic() + keyword1 + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + keyword2 + "\n\nNo articles found\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_refine_search_first_keyword_empty(self, input_mock):
        keyword1 = ''
        keyword2 = 'computer'
        advanced_option = 6

        output = get_print(input_mock, [keyword1, advanced_option, keyword2])
        expected = print_basic() + keyword1 + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + keyword2 + "\n\nNo articles found\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_refine_search_second_keyword_empty(self, input_mock):
        keyword1 = 'Anna'
        keyword2 = ''
        advanced_option = 6

        output = get_print(input_mock, [keyword1, advanced_option, keyword2])
        expected = print_basic() + keyword1 + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + keyword2 + "\n\nNo articles found\n"

        self.assertEqual(output, expected)

    

    

# Write tests above this line. Do not remove.
if __name__ == "__main__":
    main()
