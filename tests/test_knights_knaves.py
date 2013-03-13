from unittest import TestCase
from mock import patch, call

from src.knights_knaves import Knight, Knave
from src.smart_mock import SmartMock


class KnightTestCase(TestCase):
    """
    Tests for a Knight
    """

    def test_knight_response(self):
        knight = Knight('Foo')

        r = knight.query('foo')
        self.assertEqual(r, u'We are of the same kind.')

    def test_knights_tell_truth(self):
        knight = Knight('Foo')

        self.assertEqual(True, knight.tell_truth())

    @patch.object(Knight, 'conjure_response')
    def test_echo(self, conjure_response):
        conjure_response.return_value = None
        knight = Knight('Foo')
        knight.query('foo')

        #
        # Be super sure we called query with 'foo'
        #

        # From docs:
        # http://www.voidspace.org.uk/downloads/mock-1.0.1.pdf

        #
        # Notice these all test pretty much the same thing
        #
        conjure_response.assert_called_with('foo')
        conjure_response.assert_called_once_with('foo')
        conjure_response.assert_any_call('foo')

        #
        # Also, notice these all test pretty much the same thing
        #
        self.assertEqual(conjure_response.called, True)
        self.assertEqual(conjure_response.call_count, 1)

        calls = [call('foo')]
        conjure_response.assert_has_calls(calls)

        #
        # But what about this?
        #
        conjure_response.assert_called_once()
        conjure_response.assert_called_once('foo')

        #
        # Or this?
        #
        conjure_response.assert_called_twice_with('foo')

        #
        # Note that these still pass, and are very subtly
        # different than their correct counterparts
        #
        # As suggested with the title of this talk:
        # Your tests may be lying to you!
        #

        #
        # Of course you may point out, that of course these
        # assertions pass. They are methods on a mock object
        # which can have anything stubbed in. This is clearly a
        # developer error you say! RTFM!
        #

        #
        # I have RTFM, many times. But I, like the rest of you
        # get tired, lazy, etc. and trying to remember which is
        # the correct signature of these mock assertions can be hard.
        #

        #
        # You may ask, what is the cost and impact of such an innocuous mistake?
        #
        # Hopefully small with a suite of tests covering many
        # aspects of your application. But in my opinion it is not OK
        # for such a simple mistake to be made, which is hard to track down
        # once your app starts failing in non-obvious ways even though "the tests pass" giving
        # developers a false sense of security

        #
        # As an aside: I think "but the tests pass" is the new "but it works on my machine"
        # but that could be the topic for another TIP BOF talk altogether.
        #

        #
        # Why are there so many ways to test the same thing and why is the API not symmetrical
        # or offer more generic ways to achieve these ends?
        #

        # For example, why can't we have things like these?
        #
        # conjure_response.assert_called_with(times=3, 'foo')
        # conjure_response.assert_called_with(times=0, 'foo')
        # conjure_response.assert_never_called_with('foo')
        # etc...
        #
        # Also, any mock method with assert_* should throw an error if it is not
        # a valid method in the Mock API
        #
        #

        #
        # It turns out we can!
        # TODO: Show patches
        #


        # Secret weapons
        #print conjure_response.mock_calls
        #print conjure_response.call_list()

class KnaveTestCase(TestCase):
    """
    Tests for a Knave
    """

    def test_knave_response(self):
        knave = Knave('Foo')

        r = knave.query('foo')
        self.assertEqual(r, u'We are of different kinds.')

    def test_knaves_always_lie(self):
        knave = Knave('Foo')

        self.assertEqual(False, knave.tell_truth())

    def test_echo(self):
        knave = Knave('Foo')
        knave.conjure_response = SmartMock(return_value=None)

        knave.query('foo')
        knave.conjure_response.assert_called_once()

        knave.query('foo')
        knave.conjure_response.assert_times_called(2)

        knave.query('foo')
        knave.conjure_response.assert_times_called_with(3, 'foo')

        knave.conjure_response.assert_times_called(3)

    def test_echo_never_called(self):
        knave = Knave('Foo')
        knave.conjure_response = SmartMock(return_value=None)

        knave.conjure_response.assert_never_called()
        knave.conjure_response.assert_times_called(0)

    @patch.object(Knave, 'conjure_response', spec=SmartMock)
    def test_echo_with_patch(self, conjure_response):
        conjure_response.return_value = None

        knave = Knave('Foo')
        knave.query('foo')

        conjure_response.assert_called_once()

        knave.query('foo')
        conjure_response.assert_times_called(2)

        knave.query('foo')
        conjure_response.assert_times_called_with(3, 'foo')

        conjure_response.assert_times_called(3)

    @patch.object(Knave, 'conjure_response', spec=SmartMock)
    def test_echo_never_called_with_patch(self, conjure_response):
        conjure_response.return_value = None

        conjure_response.assert_never_called()
        conjure_response.assert_times_called(0)

        # This is actually nonsense, and should fail!
        conjure_response.assert_this_is_nonsense()

    @patch.object(Knave, 'conjure_response', spec=SmartMock)
    def test_debug(self, conjure_response):
        conjure_response.debug()
