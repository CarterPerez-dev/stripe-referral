==================
stripe-referral
==================

**Framework Agnostic Referral Program Package with Stripe Connect Integration**

.. image:: https://img.shields.io/pypi/v/stripe-referral.svg
   :target: https://pypi.org/project/stripe-referral/
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/stripe-referral.svg
   :target: https://pypi.org/project/stripe-referral/
   :alt: Python Versions

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://github.com/CarterPerez-dev/stripe-referral/blob/main/LICENSE
   :alt: License

**CertGames.com | ©AngelaMos | 2025**

----

Overview
========

``stripe-referral`` is a production-ready, framework-agnostic Python package for building 
referral programs with automated payout processing.

Features
========

- **Framework Agnostic**: Works with Flask, FastAPI, Django, or standalone
- **Multiple Payout Methods**: Stripe Connect, Wise API, Manual bank transfers
- **Type Safe**: Full TypedDict returns and modern type hints
- **Database Agnostic**: SQLAlchemy-based (PostgreSQL, MySQL, SQLite)
- **Production Ready**: Alembic migrations, error handling, validation
- **Clean Architecture**: Repository pattern, service layer, adapter pattern

----

Quick Start
===========

Installation
------------

::

    pip install stripe-referral

Basic Usage
-----------

::

    from stripe_referral import ReferralService, get_db

    # Generate referral code
    with get_db() as db:
        result = ReferralService.create_code(
            db=db,
            user_id="user_123",
            program_key="certgames"
        )
        print(f"Your code: {result['code']}")

    # Track referral conversion
    with get_db() as db:
        tracking = ReferralService.track_referral(
            db=db,
            code="REF_ABC123",
            referred_user_id="user_456"
        )
        print(f"Earned: ${tracking['amount_earned']}")

----

Documentation
=============

Coming soon...

----

Contributing
============

See `CONTRIBUTING.rst <CONTRIBUTING.rst>`_ for development setup and guidelines.

----

License
=======

MIT License - see `LICENSE <LICENSE>`_ for details.

----

Security
========

See `SECURITY.rst <SECURITY.rst>`_ for our security policy and how to report vulnerabilities.
