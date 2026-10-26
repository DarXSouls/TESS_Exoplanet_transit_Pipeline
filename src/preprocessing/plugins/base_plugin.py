"""
==========================================================
Representation Generation Layer (RGL)

Base plugin interface used throughout the preprocessing
framework.

Every plugin in the framework inherits from this class,
providing a common metadata contract while leaving the
scientific implementation to the specialised interfaces.

Author : Shyam Girish Chinta
==========================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping
from typing import Any, Hashable


 
# Base Plugin

class BasePlugin(ABC):
    """
    Abstract base class for every preprocessing plugin.

    This class defines the metadata that every plugin
    must expose. Scientific behaviour is implemented by
    specialised plugin interfaces such as selectors,
    transforms, metrics and comparison strategies.
    """

    @property
    @abstractmethod
    def id(self) -> Hashable:
        """
        Unique framework identifier for the plugin.

        Returns
        -------
        Hashable
            A framework identifier (e.g. SelectorID,
            TransformID, MetricID or ComparisonID).
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Human-readable plugin name.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def description(self) -> str:
        """
        Short description of the plugin.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def version(self) -> tuple[int, int, int]:
        """
        Plugin semantic version as
        (major, minor, patch).
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def enabled(self) -> bool:
        """
        Whether this plugin should be available
        for registration.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def default_config(self) -> Mapping[str, Any]:
        """
        Default plugin configuration.

        Returns
        -------
        Mapping[str, Any]
            Read-only default configuration for the
            plugin.
        """
        raise NotImplementedError