Feature: current-weather
  Scenario: current local weather
    Given an English speaking user
     When the user says "tell me the weather"
     Then "my-weather-skill" should reply with "Right now, it's overcast clouds and 32 degrees."