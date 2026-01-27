import aws_cdk as core
import aws_cdk.assertions as assertions

from employee_directory_app.employee_directory_app_stack import EmployeeDirectoryAppStack

# example tests. To run these tests, uncomment this file along with the example
# resource in employee_directory_app/employee_directory_app_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = EmployeeDirectoryAppStack(app, "employee-directory-app")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
