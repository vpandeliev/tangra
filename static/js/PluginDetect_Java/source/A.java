/*    By Eric Gerds


 getJavaInfo.jar v3
 ----------------------
 We added getAppVersion() method to return the version of this jarfile.
 We also no longer compress the jarfile using jarg.jar (or any other 3rd party compression tool)
 in order to improve compatibility/reliability.


 getJavaInfo.jar v2
 ---------------------
 Rename getInfo() to getProp()


 getJavaInfo.jar v2 beta1
 -------------------------
 We added 2 more methods to the applet.
    getInfo(String S) - returns value of System.getProperty(S)
    statusbar() - sets the value of the browser status bar from Java.
       This only works sometimes depending on the browser, but it could allow you to
       overwrite the "Applet Started" message in the status bar when an applet starts up.
 This applet is backwards compatible with any Javascripts that use getJavaInfo.jar v1.


 getJavaInfo.jar v1
 ---------------------
 The very first version of our jar. Has 2 public methods:
     getVersion() - returns Java version
     getVendor() - returns Java vendor


*/

import java.applet.*;

 public class A extends Applet
 {

    public String getAppVersion()
    {
       return "3";      // version of this applet
    }

    public String getProp(String S)
    {
       String o="";
       try{
           if (S instanceof String) o=System.getProperty(S);
       }
       catch(Exception e){};
       return o;
    }

    public String getVersion()
    {
       return getProp("java.version");
    }

    public String getVendor()
    {
       return getProp("java.vendor");
    }

    
/*  Set the browser window status bar from within this applet.

    We would like to prevent the window status bar from showing the "Applet A started"
    message when detecting Java. This message only occurs in some browsers, not all.
    We can solve this problem using the showStatus("") method from within the Java applet.

    - Is the showStatus method compatible with Java 1.3?

    - Even when you cannot set window.status from Javascript, it is still possible
     in some browsers for the applet to affect the status bar. Hence it is probably best
     to set the status bar from within the applet using showStatus().

    - Note, some browsers show the word "Done" in the status bar after the page has fully
    loaded (ie. window.onload has fired). We want to avoid overwriting the 'Done'.

*/
    public void statusbar(String S)
    {
       try{
           if (S instanceof String) showStatus(S);
       }
       catch(Exception e){};
    }


 }
