"""
==========================================================
Representation Generation Layer (RGL)

Generic registry used throughout the preprocessing
framework.

Stores objects identified by unique identifiers.

Author : Shyam Girish Chinta
Project: ISRO Exoplanet Detection Pipeline
==========================================================
"""

from __future__ import annotations

from collections.abc import (
    Iterator,
    KeysView,
    Mapping,
    ItemsView,
    ValuesView,
)
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Generic, TypeVar



# Generic Type Variables

ID = TypeVar("ID")

T = TypeVar("T")



# Base Registry

@dataclass(slots=True)
class BaseRegistry(Generic[ID, T]):
    """
    Generic registry for storing objects identified by a
    unique identifier.

    The registry provides type-safe registration and
    lookup while exposing a read-only view of its
    contents.
    """

    _objects: dict[ID, T] = field(
        default_factory=dict,
        init=False,
        repr=False,
    )

     
    # Registration

    def register(
        self,
        identifier: ID,
        obj: T,
    ) -> T:
        """
        Register an object.

        Parameters
        ----------
        identifier
            Unique object identifier.

        obj
            Object to register.

        Returns
        -------
        T
            The registered object.

        Raises
        ------
        ValueError
            If the identifier already exists.
        """

        if identifier in self._objects:
            raise ValueError(
                f"Duplicate registration: {identifier!r}"
            )

        self._objects[identifier] = obj

        return obj

     
    # Lookup   

    def get(
        self,
        identifier: ID,
    ) -> T:
        """
        Retrieve a registered object.

        Raises
        ------
        KeyError
            If the identifier is not registered.
        """

        try:
            return self._objects[identifier]

        except KeyError as exc:
            raise KeyError(
                f"Unknown identifier: {identifier!r}"
            ) from exc

     
    # Utilities 

    def clear(self) -> None:
        """
        Remove all registered objects.
        """

        self._objects.clear()

    @property
    def mapping(self) -> Mapping[ID, T]:
        """
        Read-only view of the registry.
        """

        return MappingProxyType(self._objects)

    def keys(self) -> KeysView[ID]:
        """
        Registered identifiers.
        """

        return self._objects.keys()

    def values(self) -> ValuesView[T]:
        """
        Registered objects.
        """

        return self._objects.values()

    def items(self) -> ItemsView[ID, T]:
        """
        Registered identifier-object pairs.
        """

        return self._objects.items()

    def ids(
        self,
    ) -> tuple[ID, ...]:
        """
        Return all registered identifiers.
        """

        return tuple(
            self._objects.keys()
        )

     
    # Python Protocols

    def __contains__(
        self,
        identifier: ID,
    ) -> bool:

        return identifier in self._objects

    def __len__(self) -> int:

        return len(self._objects)

    def __iter__(self) -> Iterator[ID]:

        return iter(self._objects)