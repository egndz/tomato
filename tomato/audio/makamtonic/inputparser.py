#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2015 - 2018 Altuğ Karakurt & Sertan Şentürk
#
# This file is part of tomato: https://github.com/sertansenturk/tomato/
#
# tomato is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation (FSF), either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU Affero General Public License v3.0
# along with this program. If not, see http://www.gnu.org/licenses/
#
# If you are using this extractor please cite the following paper:
#
# Karakurt, A., Şentürk S., and Serra X. (2016). MORTY: A toolbox for mode
# recognition and tonic identification. In Proceedings of 3rd International
# Digital Libraries for Musicology Workshop (DLfM 2016). pages 9-16,
# New York, NY, USA

import copy
import logging

import numpy as np

from ..pitchdistribution import PitchDistribution
from ...converter import Converter

logger = logging.Logger(__name__, level=logging.INFO)


class InputParser:
    _dummy_ref_freq = 220.0

    def __init__(self, step_size=7.5, kernel_width=7.5, feature_type='pcd',
                 model=None):
        """--------------------------------------------------------------------
        These attributes are wrapped as an object since these are used in both
        training and estimation stages and must be consistent in both processes
        -----------------------------------------------------------------------
        step_size       : Step size of the distribution bins
        kernel_width    : Standard deviation of the gaussian kernel used to
                          smoothen the distributions.
        feature_type    : The feature type to be used in training and testing
                          ("pd" for pitch distribution, "pcd" for pitch
                          class distribution)
        --------------------------------------------------------------------"""
        self.kernel_width = kernel_width
        self.step_size = step_size

        assert feature_type in ['pd', 'pcd'], \
            '"feature_type" can either take the value "pd" (pitch ' \
            'distribution) or "pcd" (pitch class distribution).'
        self.feature_type = feature_type

        if model is not None:
            assert all(m['feature'].distrib_type() == feature_type
                       for m in model), 'The feature_type input and type ' \
                                        'of the distributions in the ' \
                                        'model input does not match'
        self.model = model

    def _parse_tonic_and_joint_estimate_input(self, test_input):
        if isinstance(test_input, PitchDistribution):  # pitch distribution
            assert test_input.has_hz_bin(), 'The input distribution has a ' \
                                            'reference frequency already.'
            input_copy = copy.deepcopy(test_input)
            input_copy.hz_to_cent(self._dummy_ref_freq)
            return input_copy

        # pitch track or file
        pitch_cent = self._parse_pitch_input(test_input, self._dummy_ref_freq)
        return self._cent_pitch_to_feature(pitch_cent, self._dummy_ref_freq)

    def _parse_mode_estimate_input(self, feature_in, tonic=None):
        if isinstance(feature_in, PitchDistribution):
            feature = copy.deepcopy(feature_in)
            if tonic is not None:  # tonic given
                feature.hz_to_cent(tonic)
        else:  # pitch
            if tonic is None:  # pitch given in cent units
                pitch_cent = feature_in
                ref_freq = self._dummy_ref_freq
            else:  # tonic given.
                pitch_cent = self._parse_pitch_input(feature_in, tonic)
                ref_freq = tonic
            feature = self._cent_pitch_to_feature(pitch_cent, ref_freq)

        return feature

    @staticmethod
    def _parse_pitch_input(pitch_in, tonic_freq):
        """
        Parses the pitch input from list, numpy array or file.

        If the input (or the file content) is a matrix, the method assumes the
        columns represent timestamps, pitch and "other columns".
        respectively. It only returns the second column in this case.

        :param pitch_in: pitch input, which is a list, numpy array or filename
        :param tonic_freq: the tonic frequency in Hz
        :return: parsed pitch track (numpy array)
        """
        # parse the pitch track from txt file, list or numpy array
        try:
            p = np.loadtxt(pitch_in)
        except ValueError:
            logger.debug('pitch_in is not a filename')
            p = np.array(pitch_in)

        p = p[:, 1] if p.ndim > 1 else p  # get the pitch stream

        # normalize wrt tonic
        return Converter.hz_to_cent(p, tonic_freq)

    def _cent_pitch_to_feature(self, pitch_cent, ref_freq):
        feature = PitchDistribution.from_cent_pitch(
            pitch_cent, ref_freq=ref_freq, kernel_width=self.kernel_width,
            step_size=self.step_size)
        if self.feature_type == 'pcd':
            feature.to_pcd()

        return feature
