Feature: Say model
   Scenario: Test smoke
    Given an English speaking user
     When the user says "Give me the tomato"
     Then mycroft reply should contain "tomato"

   Scenario: User ask for problem
    Given an English speaking user
     When the user says "next release problem"
     Then mycroft reply should contain "Your profit will be"
   
   Scenario: User asks for next requirement to implement 
    Given an English speaking user
     When the user says "What is the next requirement to implement"
     Then mycroft reply should contain "The next requirements to implement are"

   Scenario: User asks for stakeholder satisfaction
    Given an English speaking user
     When the user says "Client satisfaction"
     Then mycroft reply should contain "Stakeholder satisfied are"
   
   Scenario: User asks for costs
    Given an English speaking user
     When the user says "How much the implementation will cost"
     Then mycroft reply should contain "The cost will be"
   
   Scenario: User asks for state to be deleted
    Given an English speaking user
     When the user says "Delete saved state"
     Then mycroft reply should contain "Internal state deleted"


   Scenario: User ask for problem with cost 
    Given an English speaking user
     When the user says "next release problem with 200 dollars max"
     Then mycroft reply should contain "985"
   
