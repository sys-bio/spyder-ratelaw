# -*- coding: utf-8 -*-
#
# Copyright © 2017 Kiri Choi and Jayit Biswas
# Based on Spyder by Spyder Project Contributors
# Licensed under the terms of the MIT License
#
# Rate Law Plugin
#
#    - Basic implementation of Rate Law Library plugin
#    - Shows example of how to add Hello World to the External Tools menu, e.g.
#        Tools -> External Tools
#        RateLaw item to theConfiguration Page, e.g.
#        Tools -> Preferences

from __future__ import print_function, division

# Standard library imports
import os.path as osp

# Third party imports
from qtpy.QtCore import Signal
from qtpy.QtWidgets import QGroupBox, QLabel, QVBoxLayout
from spyder.config.base import get_translation
from spyder.plugins import SpyderPluginMixin
from spyder.plugins.configdialog import PluginConfigPage
from spyder.utils.qthelpers import create_action, get_icon
from .widgets.ratelawgui import RateLawWidget

_ = get_translation("ratelaw", "spyder_ratelaw")

class RateLawConfigPage(PluginConfigPage):
    """
    The Configuration Page that can be found under Tools -> Preferences. This
    only displays a label. 
    """
    
    def setup_page(self):
        """ Setup of the configuration page. All widgets need to be added here"""
        
        setup_group = QGroupBox(_("RateLaw Plugin Configuration"))
        setup_label = QLabel(_("RateLaw plugin configuration needs to be "\
                               "implemented here.\n"))
        setup_label.setWordWrap(True)

        # Warning: do not try to regroup the following QLabel contents with 
        # widgets above -- this string was isolated here in a single QLabel
        # on purpose: to fix Issue 863
        setup_layout = QVBoxLayout()
        setup_layout.addWidget(setup_label)
        setup_group.setLayout(setup_layout)

        vlayout = QVBoxLayout()
        vlayout.addWidget(setup_group)
        vlayout.addStretch(1)
        self.setLayout(vlayout)

class RateLaw(RateLawWidget, SpyderPluginMixin):
    """RateLaw class that implements all the SpyderPluginMixin methods"""
    CONF_SECTION = 'ratelaw'
    CONFIGWIDGET_CLASS = RateLawConfigPage
    edit_goto = Signal(str, int, str)
    
    def __init__(self, parent=None):
        RateLawWidget.__init__(self, parent=parent)
        SpyderPluginMixin.__init__(self, parent)
        
        # Initialize plugin
        self.initialize_plugin()
        
    #------ SpyderPluginWidget API ---------------------------------------------    
    def get_plugin_title(self):
        """Return widget title"""
        return _("RateLaw")

    def get_plugin_icon(self):
        """Return widget icon"""
        path = osp.join(self.PLUGIN_PATH, self.IMG_PATH)
        return get_icon(osp.join(path, 'ratelaw.png'))
    
    def get_focus_widget(self):
        """
        Return the widget to give focus to when
        this plugin's dockwidget is raised on top-level
        """
        pass
    
    def get_plugin_actions(self):
        """Return a list of actions related to plugin"""
        return []

    def on_first_registration(self):
        """Action to be performed on first plugin registration"""
        self.main.tabify_plugins(self.main.help, self)
        self.dockwidget.hide()

    def register_plugin(self):
        """Register plugin in Spyder's main window"""
        self.edit_goto.connect(self.main.editor.load)
        self.redirect_stdio.connect(self.main.redirect_internalshell_stdio)
        self.main.add_dockwidget(self)
        
        ratelaw_act = create_action(self, _("Rate Law Library"),
                                    icon=self.get_plugin_icon(),
                                    triggered=self.show)
        ratelaw_act.setEnabled(True)
        self.main.tools_menu_actions += [ratelaw_act]
        
    def refresh_plugin(self):
        """Refresh helloworld widget"""
        #self.remove_obsolete_items()  # FIXME: not implemented yet
        pass
    
    def closing_plugin(self, cancelable=False):
        """Perform actions before parent main window is closed"""
        return True
    
    def apply_plugin_settings(self, options):
        """Apply configuration file's plugin settings"""
        pass
    
    #------ Public API ---------------------------------------------------------    
    # Insert text into the editor window
    def show(self):
        """Show the ratelaw dockwidget"""
        if self.dockwidget and not self.ismaximized:
            self.dockwidget.setVisible(True)
            self.dockwidget.setFocus()
            self.dockwidget.raise_()
           
    def insertText(self,inserttest):
        """Accesses console to paste text"""
        checkinsert = inserttest
        self.main.editor.get_current_editor().insert_text(checkinsert)
