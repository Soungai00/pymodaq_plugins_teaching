
from typing import Union, List, Dict
from pymodaq.control_modules.move_utility_classes import (DAQ_Move_base, comon_parameters_fun,
                                                          main, DataActuatorType, DataActuator)
from pymodaq_utils.utils import ThreadCommand  # object used to send info back to the main thread
from pymodaq_gui.parameter import Parameter
from pymodaq_plugins_teaching.hardware.spectrometer import Spectrometer


class DAQ_Move_Monochromator(DAQ_Move_base):
    """ Instrument plugin class for an actuator.
    
    This object inherits all functionalities to communicate with PyMoDAQ’s DAQ_Move module through inheritance via
    DAQ_Move_base. It makes a bridge between the DAQ_Move module and the Python wrapper of a particular instrument.

    TODO Complete the docstring of your plugin with:
        * The set of controllers and actuators that should be compatible with this instrument plugin.
        * With which instrument and controller it has been tested.
        * The version of PyMoDAQ during the test.
        * The version of the operating system.
        * Installation instructions: what manufacturer’s drivers should be installed to make it run?

    Attributes:
    -----------
    controller: object
        The particular object that allow the communication with the hardware, in general a python wrapper around the
         hardware library.

    """
    is_multiaxes = False
    _axis_names: Union[List[str], Dict[str, int]] = ['']
    _controller_units: Union[str, List[str]] = 'nm'
    _epsilon: Union[float, List[float]] = 0.1
    data_actuator_type = DataActuatorType.DataActuator

    params = ([{'title': 'Info', 'name': 'info', 'type': 'str', 'value': '', 'readonly': True},
               {'title': 'Gratings', 'name': 'gratings', 'type': 'list', 'limits': Spectrometer.gratings,
                'value':Spectrometer.gratings[0]},
               {'title': 'Tau', 'name': 'tau', 'type': 'float', 'value': 0.},
               {'title': 'Offset Mono', 'name': 'offset', 'type': 'float', 'value': 0., 'suffix': 'nm'}]
              + comon_parameters_fun(is_multiaxes, axis_names=_axis_names, epsilon=_epsilon))

    def ini_attributes(self):
        self.controller: Spectrometer = None
        self.offset = 0.

    def get_actuator_value(self):
        """Get the current value from the hardware with scaling conversion.

        Returns
        -------
        float: The position obtained after scaling conversion.
        """
        pos = DataActuator(data=self.controller.get_wavelength())  # when writing your own plugin replace this line
        pos = self.get_position_with_scaling(pos)
        return pos

    def close(self):
        """Terminate the communication protocol"""
        self.controller.close_communication()

    def commit_settings(self, param: Parameter):
        """Apply the consequences of a change of value in the detector settings

        Parameters
        ----------
        param: Parameter
            A given parameter (within detector_settings) whose value has been changed by the user
        """
        if param.name() == 'axis':
            self.axis_unit = self.controller.get_wavelength_axis()
        elif param.name() == 'gratings':
            self.controller.grating(self.settings.child('gratings').value())
            self.get_actuator_value()
        elif param.name() == 'tau':
            self.controller.tau = self.settings.child('tau').value()
        elif param.name() == 'offset':
            self.offset = self.settings.child('offset').value()
        else:
            pass

    def ini_stage(self, controller=None):
        """Actuator communication initialization

        Parameters
        ----------
        controller: (object)
            custom object of a PyMoDAQ plugin (Slave case). None if only one actuator by controller (Master case)

        Returns
        -------
        info: str
        initialized: bool
            False if initialization failed otherwise True
        """
        if self.is_master:  # is needed when controller is master
            self.controller = Spectrometer()
        self.settings.child('info').setValue(self.controller.infos)
        self.controller.find_reference()
        info = "Whatever info you want to log"
        initialized = self.controller.open_communication()
        return info, initialized

    def move_abs(self, value: DataActuator):
        """ Move the actuator to the absolute target defined by value

        Parameters
        ----------
        value: (float) value of the absolute target positioning
        """

        value = self.check_bound(value+DataActuator(name='myoffset',
                                                    data=self.offset,
                                                    units='nm'))
        self.target_value = value
        value = self.set_position_with_scaling(value)

        self.controller.set_wavelength(value.value())
        self.emit_status(ThreadCommand('Update_Status', ['Value set']))

    def move_home(self,  value: DataActuator):
        """Call the reference method of the controller"""
        self.controller.find_reference()
        self.emit_status(ThreadCommand('Update_Status', ['Back to home']))

    def stop_motion(self):
      """Stop the actuator and emits move_done signal"""

      self.controller.stop()
      self.emit_status(ThreadCommand('Update_Status', ['Motion stopped']))


if __name__ == '__main__':
    main(__file__)
