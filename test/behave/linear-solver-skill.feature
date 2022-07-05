Feature: Say model
   Scenario: Test test/intent
    Given an English speaking user
     When the user says "Give me the tomato"
     Then mycroft reply should contain "tomato"

   Scenario: User ask for problem
    Given an English speaking user
     When the user says "release planning problem"
     Then mycroft reply should contain "Your benefit will be"
   
   Scenario: User asks for variable values 
    Given an English speaking user
     When the user says "Variable values of saved model"
     Then mycroft reply should contain "The variable values are"

   Scenario: User asks for slack values 
    Given an English speaking user
     When the user says "tell me slack values"
     Then mycroft reply should contain "The slack values are"
   
   Scenario: User asks for constraints 
    Given an English speaking user
     When the user says "What are the constraint values"
     Then mycroft reply should contain "You cannot have more"
   
   Scenario: User wants to change a constraint value 
    Given an English speaking user
     When the user says "Change constaint costs to 20"
     Then mycroft reply should contain "Constraint costs updated to 20"
   
   Scenario: User wants to change a variable value 
    Given an English speaking user
     When the user says "Increase cars by one"
     Then mycroft reply should contain "Done. New benefit is"

   Scenario: User ask for state to be deleted
    Given an English speaking user
     When the user says "delete state"
     Then mycroft reply should contain "Internal state deleted"