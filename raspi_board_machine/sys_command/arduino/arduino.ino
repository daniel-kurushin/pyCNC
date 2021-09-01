
void setup() 
{
  Serial.begin(9600); 
  Serial.setTimeout(10);
  pinMode(13, OUTPUT);
}

float data = 0;
int state_begin, state_end;
String input;

void loop() 
{
  if(Serial.available() > 0)
  {
    input = Serial.readStringUntil('\n');
  }
  if(input.indexOf('\n'))
  {
    for(int i = 0; i < 10; i++)
    {
      digitalWrite(13, !digitalRead(13));
      delay(100);
    }
    input = "";
  }
  
  /*
  String pars = "{'state': 'ready', 'cmd': 'wait', 'data': 0}";
  String pars_state = "'state' : 'ready',";
  String pars_cmd = "'cmd' : 'wait',";
  String pars_data = "'data' : '0'";
  String state, cmd, data;

  state_begin = pars_state.indexOf("'", pars_state.indexOf(':'));
  state_end = pars_state.lastIndexOf("'");
  for(int i = state_begin + 1; i < state_end; i++)
  {
    state.concat(pars_state[i]);
  }

  state_begin = pars_cmd.indexOf("'", pars_cmd.indexOf(':'));
  state_end = pars_cmd.lastIndexOf("'");
  for(int i = state_begin + 1; i < state_end; i++)
  {
    cmd.concat(pars_cmd[i]);
  }

  state_begin = pars_data.indexOf("'", pars_data.indexOf(':'));
  state_end = pars_data.lastIndexOf("'");
  for(int i = state_begin + 1; i < state_end; i++)
  {
    data.concat(pars_data[i]);
  }
  
  Serial.println(state);
  Serial.println(cmd);
  Serial.println(data);
  while(1);
  */
}
