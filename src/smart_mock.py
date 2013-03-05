from mock import (DEFAULT, _patch, ClassTypes, _callable,
                  NonCallableMagicMock, NonCallableMock, _is_instance_mock,
                  _is_list, _instance_callable,
                  mocksignature, patch, MagicMock, Mock, DescriptorTypes,
                  FunctionTypes, _set_signature, _check_signature,
                  _is_magic, FunctionAttributes, _SpecState, _must_skip, create_autospec)


class SmartMock(MagicMock):
    """
    Subclass MagicMock to provide a few smarter assertions
    """

    def _pluralization(self, times):
        return 'times' if times != 1 else 'time'

    def debug(self):
        print
        print "*" * 50
        print 'Type: ', type(self)
        print 'Call Count: ', str(self.call_count)
        print 'Mock Calls: ', self.mock_calls
        print 'Call List: ' , self.call_list()
        print "*" * 50
        print

        raise

    # Derived assertions
    def assert_never_called(_mock_self, *args, **kwargs):
        self = _mock_self
        return self.assert_times_called(0, *args, **kwargs)

    def assert_called_once(_mock_self, *args, **kwargs):
        self = _mock_self
        return self.assert_times_called(1, *args, **kwargs)


    # Primitive times assertions
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


class _smart_patch(_patch):
    """
    Subclass _patch to provide a custom behavior
    """

    def __enter__(self):
        """
        Overrides base, perform the patch with SmartMock.
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

            ### Use SmartMock here ###
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

#def create_autospec(spec, spec_set=False, instance=False, _parent=None,
#                    _name=None, **kwargs):
#    #
#    # Overrides base, perform the patch with SmartMock.
#    #
#    if _is_list(spec):
#        # can't pass a list instance to the mock constructor as it will be
#        # interpreted as a list of strings
#        spec = type(spec)
#
#    is_type = isinstance(spec, ClassTypes)
#
#    _kwargs = {'spec': spec}
#    if spec_set:
#        _kwargs = {'spec_set': spec}
#    elif spec is None:
#        # None we mock with a normal mock without a spec
#        _kwargs = {}
#
#    _kwargs.update(kwargs)
#
#    ### Use SmartMock here ###
#    Klass = SmartMock
#
#    if type(spec) in DescriptorTypes:
#        # descriptors don't have a spec
#        # because we don't know what type they return
#        _kwargs = {}
#    elif not _callable(spec):
#        Klass = NonCallableMagicMock
#    elif is_type and instance and not _instance_callable(spec):
#        Klass = NonCallableMagicMock
#
#    _new_name = _name
#    if _parent is None:
#        # for a top level object no _new_name should be set
#        _new_name = ''
#
#    mock = Klass(parent=_parent, _new_parent=_parent, _new_name=_new_name,
#        name=_name, **_kwargs)
#
#    if isinstance(spec, FunctionTypes):
#        # should only happen at the top level because we don't
#        # recurse for functions
#        mock = _set_signature(mock, spec)
#    else:
#        _check_signature(spec, mock, is_type, instance)
#
#    if _parent is not None and not instance:
#        _parent._mock_children[_name] = mock
#
#    if is_type and not instance and 'return_value' not in kwargs:
#        # XXXX could give a name to the return_value mock?
#        mock.return_value = create_autospec(spec, spec_set, instance=True,
#            _name='()', _parent=mock)
#
#    for entry in dir(spec):
#        if _is_magic(entry):
#            # MagicMock already does the useful magic methods for us
#            continue
#
#        if isinstance(spec, FunctionTypes) and entry in FunctionAttributes:
#            # allow a mock to actually be a function from mocksignature
#            continue
#
#        # XXXX do we need a better way of getting attributes without
#        # triggering code execution (?) Probably not - we need the actual
#        # object to mock it so we would rather trigger a property than mock
#        # the property descriptor. Likewise we want to mock out dynamically
#        # provided attributes.
#        # XXXX what about attributes that raise exceptions on being fetched
#        # we could be resilient against it, or catch and propagate the
#        # exception when the attribute is fetched from the mock
#        original = getattr(spec, entry)
#
#        kwargs = {'spec': original}
#        if spec_set:
#            kwargs = {'spec_set': original}
#
#        if not isinstance(original, FunctionTypes):
#            new = _SpecState(original, spec_set, mock, entry, instance)
#            mock._mock_children[entry] = new
#        else:
#            parent = mock
#            if isinstance(spec, FunctionTypes):
#                parent = mock.mock
#
#            new = SmartMock(parent=parent, name=entry, _new_name=entry,
#                _new_parent=parent, **kwargs)
#            mock._mock_children[entry] = new
#            skipfirst = _must_skip(spec, entry, is_type)
#            _check_signature(original, new, skipfirst=skipfirst)
#
#        # so functions created with mocksignature become instance attributes,
#        # *plus* their underlying mock exists in _mock_children of the parent
#        # mock. Adding to _mock_children may be unnecessary where we are also
#        # setting as an instance attribute?
#        if isinstance(new, FunctionTypes):
#            setattr(mock, entry, new)
#
#    return mock


def _smart_mock(
        target, attribute, new=DEFAULT, spec=SmartMock,
        create=False, mocksignature=False, spec_set=True, autospec=False,
        new_callable=None, **kwargs):
    """
    Create decorator/callable for our smart mock
    """
    getter = lambda: target

    return _smart_patch(
        getter, attribute, new, spec, create, mocksignature,
        spec_set, autospec, new_callable, kwargs
    )

# Inject into patch
#patch.object = _smart_mock
patch.smart_object = _smart_mock