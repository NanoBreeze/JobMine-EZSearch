"""
This file is part of JobMine EZSearch.

JobMine EZSearch is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

JobMine EZSearch is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with JobMine EZSearch.  If not, see <http://www.gnu.org/licenses/>.
"""

import pip

print("Installing")
pip.main(['install',  'requests'])
pip.main(['install', 'bs4'])
pip.main(['install', 'flask'])
pip.main(['install', 'pycrypto'])
pip.main(['install', 'python-docx'])


import setup
