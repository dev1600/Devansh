#include <stdio.h>
#include <math.h>

#define pi 3.14159
void main()
{
   int i=0;
   float link[3]={1.0,1.0,1.0};       //Enter length of Links
   float theta[3]={-45.58,-88.85,224.42};   //Enter Angles

   for(i=0;i<3;i++)
   {
       theta[i]=theta[i]*pi/180;
   }

   float c1=cos(theta[0]);
   float c12=cos(theta[0]+theta[1]);
   float c123=cos(theta[0]+theta[1]+theta[2]);

   float s1=sin(theta[0]);
   float s12=sin(theta[0]+theta[1]);
   float s123=sin(theta[0]+theta[1]+theta[2]);

   float Ex=link[0]*c1+link[1]*c12+link[2]*c123;
   float Ey=link[0]*s1+link[1]*s12+link[2]*s123;

   printf("END EFFECTOR X:%f",Ex);
   printf("\nEND EFFECTOR Y:%f",Ey);

}
