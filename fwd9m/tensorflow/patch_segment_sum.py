# Copyright 2020 NVIDIA Corporation. All Rights Reserved
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
# ========================================================================

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf

from tensorflow.python.eager import context
from tensorflow.python.framework import ops
from tensorflow.python.ops import gen_math_ops
from tensorflow.python.ops import math_ops

def _patch_segment_sum():
  _new_segment_sum.__doc__ = tf.math.segment_sum.__doc__
  math_ops.segment_sum = _new_segment_sum # access via public API
  tf.math.segment_sum = _new_segment_sum # access via public API

# The original, pre-patched function is automatically-generated. Therefore, we
# cannot provide a URL to its location in the source repository.
# For the history of this patch, please refer to
# https://github.com/tensorflow/tensorflow/issues/39751
def _new_segment_sum(data, segment_ids, name=None):
  """ERROR: docstring should have been added programatically. """
  with ops.name_scope(name, "SegmentSum", [data, segment_ids]) as name:
    # Note that data can be a vector-like list (or an n-dimensional
    # tensor-like list of lists). We convert to tensor here to replicate the
    # behavior of the pre-existing op.
    data = tf.convert_to_tensor(data)

    # Note that this patch does not provide determinism when the dtype of the
    # data argument is tf.float64 or tf.complex128.
    orig_dtype = data.dtype
    if 'float' in str(orig_dtype):
      data = tf.cast(data, dtype=tf.float64)
    elif 'complex' in str(orig_dtype):
      data = tf.cast(data, dtype=tf.complex128)

    if not context.executing_eagerly():
      data = ops.convert_to_tensor(data, name="input_data")
      segment_ids = ops.convert_to_tensor(segment_ids, name="segment_ids")

    result = gen_math_ops.segment_sum(data, segment_ids)
    return tf.cast(result, dtype=orig_dtype)
