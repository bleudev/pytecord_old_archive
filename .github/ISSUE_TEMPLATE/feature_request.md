name: Feature request
about: Suggest an idea for this project
labels: ["Feature request"]
assignees: ''
body:
  - type: input
    attributes:
    label: Description
    description: >
      A short description of your idea
    validations:
    required: true
  - type: dropdown
    attributes:
    multiple: false
    label: What is the feature request for?
    options:
      - disspy
      - The documentation
    validations:
    required: true
  - type: textarea
    attributes:
    label: The Problem
    description: >
      Your problem.
      Please try give some examples.
    validations:
    required: true