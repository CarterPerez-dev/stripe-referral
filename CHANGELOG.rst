=========
Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

----

[Unreleased]
============

Added
-----

- Initial package structure with src layout
- SQLAlchemy models for referral programs, codes, tracking, and payouts
- Repository pattern for database operations
- Service layer with TypedDict return types
- Pydantic schemas for request/response validation
- Stripe Connect payout adapter
- Wise API payout adapter
- Manual bank transfer payout adapter
- Alembic database migrations
- Comprehensive type hints throughout
- Exception hierarchy with context support
- Code generation with collision detection
- Clean package exports for easy imports

Changed
-------

Nothing yet.

Deprecated
----------

Nothing yet.

Removed
-------

Nothing yet.

Fixed
-----

Nothing yet.

Security
--------

Nothing yet.

----

[0.1.1] - 2025-01-19
====================

Changed
-------

- Relaxed dependency version constraints to use >= instead of ==

----

[0.1.0] - 2025-01-19
====================

Initial release.

Added
-----

- Core referral tracking functionality
- Multi-adapter payout system
- Database migrations support
- Framework-agnostic design
