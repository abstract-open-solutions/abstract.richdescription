Abstract Rich Description Extender
==================================

Introduction
============

This package defines a schema-extender that provides a new field "rich_description".

This is a full-text searchable text-field with a RichWidget.


How it works
============

All object types are marked as "extendarable" by custom interface IRichDescriptionExtenderable::

    <class class="Products.Archetypes.BaseObject.BaseObject">
          <implements interface=".interfaces.IRichDescriptionExtenderable" />
    </class>

Manager can choose wich types apply extender to.

By default only Folder and Page types are extended.

Field "description" will be hidden automatically.


How to use
==========

This package provides a configlet that makes possibile to choose the set
of portal-types which to attach the new field to (roo-url/@@richdescription-controlpanel).


Dependencies
============

* Plone >= 4.x
* archetypes.schemaextender


License
=======
GNU GPL v2 (see docs/LICENCE.txt for details)
