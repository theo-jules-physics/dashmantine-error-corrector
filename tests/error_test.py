import unittest
from error_detection.error_detector import (
    check_parameter_exists, 
    ComponentCharacteristics, 
    detect_error_component
)

class FunctionExistenceTest(unittest.TestCase):

    def test_component_characteristics(self):
        component = ComponentCharacteristics("Button", ["color", "size"])
        self.assertEqual(component.name, "Button", "Name should be 'Button'")
        self.assertEqual(component.parameters, ["color", "size"], "Parameters should be ['color', 'size']")
        self.assertEqual(component.errors, None, "Errors should be None")

    def test_existing_parameter(self):
        function_name = "Button"
        parameter = "color"
        self.assertTrue(check_parameter_exists(function_name, parameter), 
            "Should return True for existing function 'Button' with parameter 'color'")
        
    def test_non_existing_parameter(self):
        function_name = "Button"
        parameter = "non_existent_parameter"
        self.assertFalse(check_parameter_exists(function_name, parameter), 
            "Should return False for existing function 'Button' with non-existing parameter 'non_existent_parameter'")


class ErrorDetectionTest(unittest.TestCase):
        
    def test_error_detection_no_error(self):
        component = ComponentCharacteristics("Button", ["color", "size"])
        message = detect_error_component(component)
        self.assertEqual(message, "No errors detected for Button component", 
            "Should return 'No errors detected for Button component'")
        self.assertEqual(component.errors["count"], 0, "Error count should be 0")
        self.assertEqual(component.errors["invalid_items"], [], "Invalid items should be empty")
    
    def test_error_detection_missing_parameter(self):
        component = ComponentCharacteristics("Button", ["not_existing_parameter", "size", "not_existing_parameter_2"])
        message = detect_error_component(component)
        expected_message = "Errors detected for parameters in Button component: ['not_existing_parameter', 'not_existing_parameter_2'] do not exist"
        self.assertEqual(message, expected_message, 
            f"Should return '{expected_message}'")
        self.assertEqual(component.errors["count"], 2, "Error count should be 2")
        self.assertEqual(component.errors["invalid_items"], ["not_existing_parameter", "not_existing_parameter_2"], 
            "Invalid items should include both invalid parameters")
            
    def test_error_detection_non_existent_component(self):
        component = ComponentCharacteristics("FakeButton", ["color", "size"])
        message = detect_error_component(component)
        expected_message = "Component FakeButton does not exist"
        self.assertEqual(message, expected_message, f"Should return '{expected_message}'")
        self.assertEqual(component.errors["count"], 1, "Error count should be 1")
        self.assertEqual(component.errors["invalid_items"], ["FakeButton"], 
            "Invalid items should include the component name")
    
    def test_error_detection_error_state(self):
        # Test that errors object is properly initialized
        component = ComponentCharacteristics("Button", [])
        detect_error_component(component)
        self.assertIsNotNone(component.errors, "Errors should not be None after detection")
        self.assertIn("count", component.errors, "Errors should contain 'count' key")
        self.assertIn("message", component.errors, "Errors should contain 'message' key")
        self.assertIn("invalid_items", component.errors, "Errors should contain 'invalid_items' key")
        

if __name__ == '__main__':
    unittest.main()