
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
  String honepa, data;
  int k = 0;
  if(Serial.available() > 0)
  {
    k = Serial.read();
    if(k == 123)
    {
      while(honepa != "}")
      {
        honepa = Serial.readStringUntil('\n');
        if(honepa.length() > 1)
        {
          Serial.println(honepa);
        }
      }
      k = 0;
    }
  }
  if(honepa.length() > 0)
  {
    for(int i = 0; i < 10; i++)
    {
      digitalWrite(13, !digitalRead(13));
      delay(3000);
    }
    honepa = "";
  }
  /*
  String honepa;
  int k = 0;
  if(Serial.available() > 0)
  {
    k = Serial.read();
    if(k == 123)
    {
      while(k != 125)
      {
        k = Serial.read();
        honepa += char(k);
      }
    }
  }
  if(honepa.length() > 0)
  {
    Serial.println(honepa);
    honepa = ""; 
    while(1); 
  }
  */
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
