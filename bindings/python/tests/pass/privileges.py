#!/usr/bin/env python

# Copyright 2019 Stanford University
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from __future__ import print_function

import legion
from legion import task, R, RW, WD, N, Reduce
import numpy

@task
def main():
    assert R == R
    assert RW == RW
    assert WD == WD
    assert N == N
    assert Reduce('+') == Reduce('+')

    assert R != RW
    assert R != WD
    assert R != N
    assert Reduce('+') != Reduce('*')

    assert R('x') == R('x')
    assert R('x') != R('y')
    assert R('x') != R

    assert R + R == R
    assert R + RW == RW
    assert R + WD == WD

    assert R('x') + R('y') == R('x', 'y')
    assert R('x') + R('y') != R('y', 'x')

    assert R('x', 'y') + RW('y') == R('x') + RW('y')
    assert R('x') + RW('x', 'y') == RW('x', 'y')

    assert R + Reduce('+') == RW
    assert Reduce('+') + Reduce('*') == RW
    assert Reduce('+') + WD == WD

    assert R('x', 'y') + Reduce('+', 'y', 'z') == R('x') + RW('y') + Reduce('+', 'z')

    print(R('x'))
    print(R('x') + RW('y'))

if __name__ == '__legion_main__':
    main()
