Testing for the sets branch
===========================

    >>> import model
    >>> d = model.DataRoot(programs = ())
    >>> print(d)
    DataRoot has 0 programs on disc.
    >>> print(d.programs)
    ()
    >>> import functions
    >>> d.load_factory_soundbank()
    >>> print(d)
    DataRoot has 98 programs on disc.
    >>> print(d.programs[0].description)
    Monologue
    >>> print(d.programs[79].description)
    Apparatorium
