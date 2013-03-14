from mock import MagicMock


class SmartMock(MagicMock):
    """
    Subclass MagicMock to provide a few smarter assertions
    """

    def _pluralization(self, times):
        return 'times' if times != 1 else 'time'

    # Derived assertions
    def assert_never_called(self, *args, **kwargs):
        return self.assert_times_called(0, *args, **kwargs)

    def assert_called_once(self, *args, **kwargs):
        return self.assert_times_called(1, *args, **kwargs)

    # Primitive times assertions
    def assert_times_called(self, times, *args, **kwargs):
        if self.call_count != times:
            expected_text = self._pluralization(times)
            actual_text = self._pluralization(self.call_count)
            msg = ("Expected to be called %s %s. Actually called %s %s." %
                   (times, expected_text, self.call_count, actual_text))
            raise AssertionError(msg)

    def assert_times_called_with(self, times, *args, **kwargs):
        if self.call_count != times:
            expected_text = self._pluralization(times)
            actual_text = self._pluralization(self.call_count)
            msg = ("Expected to be called %s %s. Actually called %s %s." %
                   (times, expected_text, self.call_count, actual_text))
            raise AssertionError(msg)
        return self.assert_called_with(*args, **kwargs)
