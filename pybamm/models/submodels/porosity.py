#
# Equation classes for the electrolyte porosity
#
from __future__ import absolute_import, division
from __future__ import print_function, unicode_literals
import pybamm


class Standard(pybamm.SubModel):
    """A class that generates the expression tree for Stefan-Maxwell Diffusion in the
    electrolyte.

    Parameters
    ----------
    set_of_parameters : parameter class
        The parameters to use for this submodel

    *Extends:* :class:`ElectrolyteDiffusionModel`
    """

    def __init__(self, set_of_parameters):
        super().__init__(set_of_parameters)

    def set_differential_system(self, epsilon, j):
        param = self.set_of_parameters

        deps_dt = -param.beta_surf * j
        self.rhs = {epsilon: deps_dt}
        self.initial_conditions = {epsilon: param.eps_init}

        self.variables = {"Porosity": epsilon, "Porosity change": deps_dt}

    def set_leading_order_system(self, epsilon, j):
        param = self.set_of_parameters

        self.variables = {"Porosity": epsilon}
        for k in range(3):
            # Unpack
            eps_k = epsilon.orphans[k].orphans[0]
            j_k = j.orphans[k].orphans[0]
            beta_surf_k = param.beta_surf.orphans[k].orphans[0]
            eps_init_k = param.eps_init.orphans[k].orphans[0]
            domain = epsilon.domain[k]
            Domain = domain.capitalize()

            # Model
            deps_dt = -beta_surf_k * j_k
            self.rhs = {eps_k: deps_dt}
            self.initial_conditions = {eps_k: eps_init_k}
            self.variables.update(
                {
                    Domain + " porosity": pybamm.Broadcast(eps_k, domain),
                    Domain + " porosity change": pybamm.Broadcast(deps_dt, domain),
                }
            )
