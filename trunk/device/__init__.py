def load_device_class(device_type):
    module = __import__('.'.join(['device', device_type]))
    return getattr(getattr(module, device_type), 'ManagedDevice')
