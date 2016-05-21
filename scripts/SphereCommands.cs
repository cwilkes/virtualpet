using UnityEngine;
using System.Text;
using System.Net;
// using System.Net.Http;
using UnityEngine;
using System.Collections;

public class SphereCommands : MonoBehaviour
{
    string restEndPoint = "https://vpzkkgaonf.execute-api.us-east-1.amazonaws.com/prod/events";
   
    Vector3 originalPosition;

    // Use this for initialization
    void Start()
    {
        // Grab the original local position of the sphere when the app starts.
        originalPosition = this.transform.localPosition;
    }

    // Called by GazeGestureManager when the user performs a Select gesture
    void OnSelect()
    {
        // If the sphere has no Rigidbody component, add one to enable physics.
        if (!this.GetComponent<Rigidbody>())
        {
            var rigidbody = this.gameObject.AddComponent<Rigidbody>();
            rigidbody.collisionDetectionMode = CollisionDetectionMode.Continuous;
        }
    }

    // Called by SpeechManager when the user says the "Reset world" command
    void OnReset()
    {
        // If the sphere has a Rigidbody component, remove it to disable physics.
        var rigidbody = this.GetComponent<Rigidbody>();
        if (rigidbody != null)
        {
            DestroyImmediate(rigidbody);
        }

        // Put the sphere back into its original local position.
        this.transform.localPosition = originalPosition;
    }

    // called when user says "Pet Action"
    void OnPetAction(string[] userPetAction)
    {
        Debug.Log("OnPetAction");
        StartCoroutine(UploadPetAction(userPetAction[0], userPetAction[1], userPetAction[2]));
          // HttpClient client = new HttpClient();
          //  WebClient client = new WebClient();
          //string jsonText = @"{""user"":""chris"", ""pet"":""pet1"", ""action"":""feed""}";
          //client.UploadData(restEndPoint, "POST", Encoding.UTF8.GetBytes(jsonText));
    }

    IEnumerator UploadPetAction(string userName, string petName, string action)
    {
        Debug.Log("UploadPetAction START");
        WWWForm form = new WWWForm();
        form.AddField("user", userName);
        form.AddField("pet", petName);
        form.AddField("action", action);
        WWW w = new WWW(restEndPoint, form);
        yield return w;
        if (!string.IsNullOrEmpty(w.error))
        {
            Debug.Log("UploadPetAction ERROR: " + w.error);
        }
        else
        {
            Debug.Log("UploadPetAction GOOD");
        }
        Debug.Log("UploadPetAction DONE");
    }

    // Called by SpeechManager when the user says the "Drop sphere" command
    void OnDrop()
    {
        // Just do the same logic as a Select gesture.
        OnSelect();
    }
}