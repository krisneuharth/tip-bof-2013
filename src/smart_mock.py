from mock import (Mock, DEFAULT, _patch, ClassTypes, _callable,
                  NonCallableMagicMock, NonCallableMock, _is_instance_mock,
                  _is_list, _instance_callable, create_autospec,
                  mocksignature, patch)


class _smart_patch(_patch):
    """
    Subclass _patch to provide a custom behavior
    """

    def __enter__(self):
        """
        Overrrides base, perform the patch with SmartMock.
        """

        new, spec, spec_set = self.new, self.spec, self.spec_set
        autospec, kwargs = self.autospec, self.kwargs
        new_callable = self.new_callable
        self.target = self.getter()

        original, local = self.get_original()

        if new is DEFAULT and autospec is False:
            inherit = False
            if spec_set == True:
                spec_set = original
            elif spec == True:
                # set spec to the object we are replacing
                spec = original

            if (spec or spec_set) is not None:
                if isinstance(original, ClassTypes):
                    # If we're patching out a class and there is a spec
                    inherit = True

            # Use our custom mock
            Klass = SmartMock
            _kwargs = {}
            if new_callable is not None:
                Klass = new_callable
            elif (spec or spec_set) is not None:
                if not _callable(spec or spec_set):
                    Klass = NonCallableMagicMock

            if spec is not None:
                _kwargs['spec'] = spec
            if spec_set is not None:
                _kwargs['spec_set'] = spec_set

            # add a name to mocks
            if (isinstance(Klass, type) and
                issubclass(Klass, NonCallableMock) and self.attribute):
                _kwargs['name'] = self.attribute

            _kwargs.update(kwargs)
            new = Klass(**_kwargs)

            if inherit and _is_instance_mock(new):
                # we can only tell if the instance should be callable if the
                # spec is not a list
                if (not _is_list(spec or spec_set) and not
                _instance_callable(spec or spec_set)):
                    Klass = NonCallableMagicMock

                _kwargs.pop('name')
                new.return_value = Klass(_new_parent=new, _new_name='()',
                    **_kwargs)
        elif autospec is not False:
            # spec is ignored, new *must* be default, spec_set is treated
            # as a boolean. Should we check spec is not None and that spec_set
            # is a bool? mocksignature should also not be used. Should we
            # check this?
            if new is not DEFAULT:
                raise TypeError(
                    "autospec creates the mock for you. Can't specify "
                    "autospec and new."
                )
            spec_set = bool(spec_set)
            if autospec is True:
                autospec = original

            new = create_autospec(autospec, spec_set=spec_set,
                _name=self.attribute, **kwargs)
        elif kwargs:
            # can't set keyword args when we aren't creating the mock
            # XXXX If new is a Mock we could call new.configure_mock(**kwargs)
            raise TypeError("Can't pass kwargs to a mock we aren't creating")

        new_attr = new
        if self.mocksignature:
            new_attr = mocksignature(original, new)

        self.temp_original = original
        self.is_local = local
        setattr(self.target, self.attribute, new_attr)
        if self.attribute_name is not None:
            extra_args = {}
            if self.new is DEFAULT:
                extra_args[self.attribute_name] =  new
            for patching in self.additional_patchers:
                arg = patching.__enter__()
                if patching.new is DEFAULT:
                    extra_args.update(arg)
            return extra_args

        return new


def _smart_mock(
        target, attribute, new=DEFAULT, spec=None,
        create=False, mocksignature=False, spec_set=None, autospec=False,
        new_callable=None, **kwargs
):
    """
    Create decorator/callable for our smart mock
    """
    getter = lambda: target

    return _smart_patch(
        getter, attribute, new, spec, create, mocksignature,
        spec_set, autospec, new_callable, kwargs
    )

# Inject into patch
patch.smart_object = _smart_mock


class SmartMock(Mock):
    """
    Subclass Mock to provide a few smarter assertions
    """

    def _pluralization(self, times):
        return 'times' if times != 1 else 'time'

    # Derived assertions
    def assert_never_called(_mock_self, *args, **kwargs):
        self = _mock_self
        return self.assert_times_called(0, *args, **kwargs)

    def assert_called_once(_mock_self, *args, **kwargs):
        self = _mock_self
        return self.assert_times_called(1, *args, **kwargs)


    # Base times assertions
    def assert_times_called(_mock_self, times, *args, **kwargs):
        self = _mock_self

        if self.call_count != times:
            expected_text = self._pluralization(times)
            actual_text = self._pluralization(self.call_count)
            msg = ("Expected to be called %s %s. Actually called %s %s." %
                   (times, expected_text, self.call_count, actual_text))
            raise AssertionError(msg)

    def assert_times_called_with(_mock_self, times, *args, **kwargs):
        self = _mock_self

        if self.call_count != times:
            expected_text = self._pluralization(times)
            actual_text = self._pluralization(self.call_count)
            msg = ("Expected to be called %s %s. Actually called %s %s." %
                   (times, expected_text, self.call_count, actual_text))
            raise AssertionError(msg)
        return self.assert_called_with(*args, **kwargs)
