#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2007 Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use, modify,
# copy, or redistribute it subject to the terms and conditions of the GNU
# General Public License v.2.  This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY expressed or implied, including the
# implied warranties of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.  Any Red Hat
# trademarks that are incorporated in the source code or documentation are not
# subject to the GNU General Public License and may only be used or replicated
# with the express permission of Red Hat, Inc. 
#
import string

from pykickstart.base import *
from pykickstart.constants import *
from pykickstart.errors import *
from pykickstart.options import *

class FC6_UserData(BaseData):
    removedKeywords = BaseData.removedKeywords
    removedAttrs = BaseData.removedAttrs

    def __init__(self, *args, **kwargs):
        BaseData.__init__(self, *args, **kwargs)
        self.groups = kwargs.get("groups", [])
        self.homedir = kwargs.get("homedir", "")
        self.isCrypted = kwargs.get("isCrypted", False)
        self.name = kwargs.get("name", "")
        self.password = kwargs.get("password", "")
        self.shell = kwargs.get("shell", "")
        self.uid = kwargs.get("uid", None)

    def __str__(self):
        retval = BaseData.__str__(self)
        retval += "user"

        if len(self.groups) > 0:
            retval += " --groups=%s" % string.join(self.groups, ",")
        if self.homedir:
            retval += " --homedir=%s" % self.homedir
        if self.name:
            retval += " --name=%s" % self.name
        if self.password:
            retval += " --password=%s" % self.password
        if self.isCrypted:
            retval += " --iscrypted"
        if self.shell:
            retval += " --shell=%s" % self.shell
        if self.uid:
            retval += " --uid=%s" % self.uid

        return retval + "\n"

class F8_UserData(FC6_UserData):
    removedKeywords = FC6_UserData.removedKeywords
    removedAttrs = FC6_UserData.removedAttrs

    def __init__(self, *args, **kwargs):
        FC6_UserData.__init__(self, *args, **kwargs)
        self.lock = kwargs.get("lock", False)

    def __str__(self):
        retval = FC6_UserData.__str__(self)

        if self.lock:
            return retval.strip() + " --lock\n"
        else:
            return retval

class FC6_User(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()

        self.userList = kwargs.get("userList", [])

    def __str__(self):
        retval = ""
        for user in self.userList:
            retval += user.__str__()

        return retval

    def _getParser(self):
        def groups_cb (option, opt_str, value, parser):
            for d in value.split(','):
                parser.values.ensure_value(option.dest, []).append(d)

        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--groups", dest="groups", action="callback",
                      callback=groups_cb, nargs=1, type="string")
        op.add_option("--homedir")
        op.add_option("--iscrypted", dest="isCrypted", action="store_true",
                      default=False)
        op.add_option("--name", required=1)
        op.add_option("--password")
        op.add_option("--shell")
        op.add_option("--uid", type="int")
        return op

    def parse(self, args):
        ud = self.handler.UserData()
        (opts, extra) = self.op.parse_args(args=args)
        self._setToObj(self.op, opts, ud)
        return ud

    def dataList(self):
        return self.userList

class F8_User(FC6_User):
    removedKeywords = FC6_User.removedKeywords
    removedAttrs = FC6_User.removedAttrs

    def _getParser(self):
        op = FC6_User._getParser(self)
        op.add_option("--lock", action="store_true", default=False)
        op.add_option("--plaintext", dest="isCrypted", action="store_false")
        return op