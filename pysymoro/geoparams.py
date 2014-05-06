# -*- coding: utf-8 -*-


"""
This module contains the GeoParams data structure.
"""


from pysymoro import transform


class GeoParams(object):
    """
    Data structure:
        Represent the data structure to hold the geometric parameters.
    """
    def __init__(self, frame, params=None):
        """
        Constructor period.

        Note:
            By default the antecedent is selected as the previous frame
            (j-1). This would be automatically updated when the update()
            method is called with the correct parameters.

        Usage:
        GeoParams(frame=<frame-number>)
        GeoParams(frame=<frame-number>, params=<params-dict>)
        """
        self.frame = frame
        self.ant = frame - 1
        self.sigma = 0
        self.mu = 0
        self.gamma = 0
        self.b = 0
        self.alpha = 0
        self.d = 0
        self.theta = 0
        self.r = 0
        self.tmat = transform.TransformationMatrix(
            i=self.ant, j=self.frame
        )
        # initialise with values if available
        if params is not None:
            self.update_params(params)

    def __str__(self):
        pattern = '\t%s'
        str_format = (pattern * 11) % (
            str(self.frame), str(self.ant),
            str(self.sigma), str(self.mu),
            str(self.gamma), str(self.b),
            str(self.alpha), str(self.d),
            str(self.theta), str(self.r),
            str(self.q)
        )
        return str_format

    def __repr__(self):
        repr_format = str(self).lstrip().replace('\t', ', ')
        repr_format = '(' + repr_format + ')'
        return repr_format

    def update_params(self, params):
        """
        Update the geometric parameter values.

        Args:
            params: A dict in which the keys correspond to the list of
                parameters that are to be updated and the values
                correspond to the values with which the parameters are
                to be updated.
        """
        for key, value in params.iteritems():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(
                    "%s is not an attribute of GeoParams" % key
                )
        self.tmat.update(params)

    @property
    def q(self):
        """
        Get the joint variable value.

        Returns:
            The value of theta for a revolute joint and in the case of
            prismatic joint the value of r. For a fixed joint 0 is
            returned.
        """
        if self.sigma == 2:
            return None
        return ((1 - self.sigma) * self.theta) + (self.sigma * self.r)


