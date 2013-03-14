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
    def test_conjure_response(self, conjure_response):
        conjure_response.return_value = None
        knight = Knight('Foo')
        knight.query('foo')

        # Notice these all test pretty much the same thing
        conjure_response.assert_called_with('foo')
        conjure_response.assert_called_once_with('foo')
        conjure_response.assert_any_call('foo')

        # Also, notice these all test pretty much the same thing
        self.assertEqual(conjure_response.called, True)
        self.assertEqual(conjure_response.call_count, 1)

        calls = [call('foo')]
        conjure_response.assert_has_calls(calls)

        # But what about this?
        conjure_response.assert_called_once()
        conjure_response.assert_called_once('foo')

        # Or this?
        conjure_response.assert_called_twice_with('foo')

    @patch.object(Knight, 'conjure_response', spec=Knight)
    def test_conjure_response_with_spec(self, conjure_response):
        conjure_response.return_value = None
        knight = Knight('Foo')
        knight.query('foo')

        # This is actually nonsense, and should fail!
        conjure_response.assert_called_with_nonsense('foo')


class KnaveTestCase(TestCase):
    """
    Tests for a Knave
    """

    class TestKnave(Knave, SmartMock):
        pass

    def test_knave_response(self):
        knave = Knave('Foo')
        r = knave.query('foo')

        self.assertEqual(r, u'We are of different kinds.')

    def test_knaves_always_lie(self):
        knave = Knave('Foo')
        self.assertEqual(False, knave.tell_truth())

    def test_conjure_response(self):
        knave = Knave('Foo')

        # Use the SmartMock
        knave.conjure_response = SmartMock(return_value=None)

        knave.query('foo')
        knave.conjure_response.assert_called_once()

        knave.query('foo')
        knave.conjure_response.assert_times_called(2)

        knave.query('foo')
        knave.conjure_response.assert_times_called_with(3, 'foo')
        knave.conjure_response.assert_times_called(3)

    def test_conjure_response_never_called(self):
        knave = Knave('Foo')
        knave.conjure_response = SmartMock(return_value=None)

        knave.conjure_response.assert_never_called()
        knave.conjure_response.assert_times_called(0)

    # Use our TestKnave object to get both spec help for Knave and SmartMock
    @patch.object(Knave, 'conjure_response', spec=TestKnave)
    def test_conjure_response_with_patch(self, conjure_response):
        conjure_response.return_value = None

        knave = Knave('Foo')
        knave.query('foo')

        conjure_response.assert_called_once()

        knave.query('foo')
        conjure_response.assert_times_called(2)

        knave.query('foo')
        conjure_response.assert_times_called_with(3, 'foo')
        conjure_response.assert_times_called(3)

    @patch.object(Knave, 'conjure_response', spec=TestKnave)
    def test_conjure_response_never_called_with_patch(self, conjure_response):
        conjure_response.return_value = None

        conjure_response.assert_never_called()
        conjure_response.assert_times_called(0)

        # This is actually nonsense, and should fail!
        conjure_response.assert_this_is_nonsense()
