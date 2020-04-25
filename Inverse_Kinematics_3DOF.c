#include <stdio.h>
#include <math.h>

#define pi 3.14159
void main()
{
   int i=0;
   float link[3]={1.0,1.0,1.0};       //Enter length of Links
   float theta[3]={0};
   float Ex=1.0;                      //END EFFECTOR X Value
   float Ey=1.0;                      //END EFFECTOR Y Value

   float phi=atan(Ey/Ex);
   printf("PHI: %f",phi*180/pi);         //END EFFECTOR Angle
   float x2=Ex-link[2]*cos(phi);
   float y2=Ey-link[2]*sin(phi);

  float temp=(x2*x2+y2*y2-link[0]*link[0]-link[1]*link[1])/(2*link[0]*link[1]);
   theta[1]=(sqrt(1-temp*temp));
   theta[1]=atan(theta[1]/temp);

   temp=(((link[0]+link[1]*cos(theta[1]))*x2+link[1]*sin(theta[1])*y2)/(x2*x2+y2*y2));
   theta[0]=(((link[0]+link[1]*cos(theta[1]))*y2-(link[1]*sin(theta[1])*x2))/(x2*x2+y2*y2));
   theta[0]=atan(theta[0]/temp);

   theta[2]=phi-theta[1]-theta[0];
   printf("\nANGLE LINK-1: %f",theta[0]*180/pi);
   printf("\nANGLE LINK-2: %f",theta[1]*180/pi);
   printf("\nANGLE LINK-3: %f",theta[2]*180/pi);
}
