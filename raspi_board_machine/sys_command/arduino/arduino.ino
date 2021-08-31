
void setup() 
{
  Serial.begin(9600); 

}

float data = 0;
int state_begin, state_end;

void loop() 
{
  String pars = "{'state': 'ready', 'cmd': 'wait', 'data': 0}";
  String state, cmd, data;
  int j = 0;
  state_begin = pars.indexOf('state') + 5;
  state_end = pars.indexOf(',', pars.indexOf('state')) - 2;
  for(int i = state_begin; i <= state_end; i++)
  {
    Serial.print(pars[i]);
  }
  Serial.print('\n');
  /*
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
