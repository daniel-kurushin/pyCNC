
void setup() 
{
  Serial.begin(9600); 
  //Serial.setTimeout(10);
  pinMode(13, OUTPUT);
}

float data = 0;
int state_begin, state_end;

void loop() 
{
  
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
    /*
  state_begin = pars.indexOf('state') + 5;
  state_end = pars.indexOf(',', pars.indexOf('state')) - 2;
  for(int i = state_begin; i <= state_end; i++)
  {
    Serial.print(pars[i]);
  }
  Serial.print('\n');
  
  while(pars[j] != ',')
  {
    
    j++;
  }
  for(int i = 0; i <= pars.length(); i++)
  {
    
  }
  while(1);
  */
  while(1);
}
