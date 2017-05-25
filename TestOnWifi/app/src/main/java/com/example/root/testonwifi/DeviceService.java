package com.example.root.testonwifi;
import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.util.*;

import android.app.Activity;
import android.net.wifi.p2p.WifiP2pDevice;
import android.net.wifi.p2p.WifiP2pInfo;
import android.os.Bundle;
import android.app.IntentService;
import android.content.Intent;
import android.os.ResultReceiver;
/**
 * Created by root on 17-5-23.
 */

public class DeviceService extends IntentService{
    private boolean serviceEnabled;
    private int port;
    private File fileToSend;
    private ResultReceiver Result;
    private WifiP2pDevice targetDevice;
    private WifiP2pInfo wifiInfo;
    private MainActivity activity;
    public DeviceService() {
        super("ClientService");
        serviceEnabled = true;
    }

    @Override
    protected void onHandleIntent(Intent intent){
        wifiInfo = (WifiP2pInfo) intent.getExtras().get("wifiInfo");
        Result = (ResultReceiver) intent.getExtras().get("Result");

        if(wifiInfo == null){
                signalActivity("No WifiInfo");
        }
        else
            {
            if(!wifiInfo.isGroupOwner){
                signalActivity("I am not GroupLeader!!!!!");
            }
            else{
                signalActivity("I am GroupLeader!!!!!");
            }
        }
    }
    public void signalActivity(String message)
    {
        Bundle b = new Bundle();
        b.putString("message", message);
        Result.send(12,b);
    }
}
