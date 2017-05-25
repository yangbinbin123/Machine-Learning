package com.example.root.testonwifi;

import android.net.wifi.WpsInfo;
import android.net.wifi.p2p.WifiP2pConfig;
import android.net.wifi.p2p.WifiP2pDevice;
import android.net.wifi.p2p.WifiP2pDeviceList;
import android.net.wifi.p2p.WifiP2pInfo;
import android.net.wifi.p2p.nsd.WifiP2pDnsSdServiceInfo;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import java.io.File;
import android.net.wifi.p2p.WifiP2pManager;
import android.net.wifi.p2p.WifiP2pManager.Channel;
import android.os.Bundle;
import android.os.ResultReceiver;
import android.app.Activity;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.view.Menu;
import android.view.View;
import android.app.Fragment;
import android.view.WindowManager;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;
import java.util.*;

import java.util.ArrayList;
public class MainActivity extends AppCompatActivity {
    private WifiP2pManager wifiManager;
    private Channel wifichannel;
    private BroadcastReceiver mReceiver;
    private IntentFilter mIntentFilter;
    private Intent DeviceFuncIntent;
    private boolean serverThreadActive;
    private WifiP2pDevice targetDevice;
    private WifiP2pInfo wifiInfo;
    final HashMap<String,String> buddies = new HashMap<String,String>();
    public final int port = 7950;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        wifiManager = (WifiP2pManager) getSystemService(Context.WIFI_P2P_SERVICE);
        wifichannel = wifiManager.initialize(this, getMainLooper(), null);
        mReceiver = new WifiBroadcastReceiver(wifiManager, wifichannel, this);
        mIntentFilter = new IntentFilter();
        mIntentFilter.addAction(WifiP2pManager.WIFI_P2P_STATE_CHANGED_ACTION);
        mIntentFilter.addAction(WifiP2pManager.WIFI_P2P_PEERS_CHANGED_ACTION);
        mIntentFilter.addAction(WifiP2pManager.WIFI_P2P_CONNECTION_CHANGED_ACTION);
        mIntentFilter.addAction(WifiP2pManager.WIFI_P2P_THIS_DEVICE_CHANGED_ACTION);
        wifiInfo = null;
        DeviceFuncIntent = null;
        Button button = (Button) findViewById(R.id.GO);
        button.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View view){
                BeGroupOwner();
                Toast.makeText(getApplicationContext(),"Be GroupOwner!!",Toast.LENGTH_SHORT).show();
            }
        });

    }
    @Override
    protected void onResume(){
        super.onResume();
        registerReceiver(mReceiver,mIntentFilter);
    }
    @Override
    protected void onPause(){
        super.onPause();
        unregisterReceiver(mReceiver);
    }

    public void setNetworkToReadyState(WifiP2pInfo info, WifiP2pDevice device)
    {
        wifiInfo = info;
        targetDevice = device;
    }



    // Discover peers
    public void searchForPeers(View view){
        wifiManager.discoverPeers(wifichannel,new WifiP2pManager.ActionListener(){
            @Override
            public void onSuccess(){
            }
            @Override
            public void onFailure(int reason){
            }
        });
    }

    public void displayPeers(final WifiP2pDeviceList peers){
        ListView peerView = (ListView)findViewById(R.id.Listpeers);
        ArrayList<String> peerList = new ArrayList<String>();
        for(WifiP2pDevice wd : peers.getDeviceList()){
            peerList.add(wd.deviceName);
        }

        peerView.setClickable(true);
        ArrayAdapter arrayAdapter = new ArrayAdapter(this, android.R.layout.simple_list_item_1,peerList.toArray());
        peerView.setAdapter(arrayAdapter);

        peerView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                TextView tv = (TextView) view;
                WifiP2pDevice device = null;

                for(WifiP2pDevice wd : peers.getDeviceList()){
                    if(wd.deviceName.equals(tv.getText())){
                        device = wd;
                    }
                }
                if(device != null){
                    connectToPeer(device);
                }
            }
        });
    }

    public void connectToPeer(final WifiP2pDevice wifiPeer){
        this.targetDevice = wifiPeer;
        WifiP2pConfig config = new WifiP2pConfig();
        config.deviceAddress = wifiPeer.deviceAddress;
        //SetWifiStatus(wifiPeer.deviceAddress);
        config.wps.setup = WpsInfo.PBC;
        if (wifiPeer.deviceAddress.equals("c2:ee:fb:ee:a1:9c")){
            config.groupOwnerIntent = 0;
            //this device has the highest priority to be group owner
        }
        else {
            config.groupOwnerIntent = 15;
        }
        wifiManager.connect(wifichannel,config,new WifiP2pManager.ActionListener(){
                public void onSuccess(){
                     //SetWifiStatus("Connection to" + targetDevice.deviceName + " sucessful");
            }
                public void onFailure(int reason){
                     //SetWifiStatus("Connection to" + targetDevice.deviceName + " failed");
            }
        });
    }
    private void BeGroupOwner(){
        wifiManager.createGroup(wifichannel, new WifiP2pManager.ActionListener(){
            @Override
            public void onSuccess(){

            }
            @Override
            public void onFailure(int reason){

            }
        });
    }

    public void DeviceFunc(View view){
        //Toast.makeText(getApplicationContext(),"DeviceFunc",Toast.LENGTH_SHORT).show();
        DeviceFuncIntent = new Intent(this,DeviceService.class);
        DeviceFuncIntent.putExtra("wifiInfo",wifiInfo);
        startService(DeviceFuncIntent);
        GroupLeaderOrNot("Test:"+wifiInfo.isGroupOwner);
        DeviceFuncIntent.putExtra("Result", new ResultReceiver(null){
           @Override
            protected void onReceiveResult(int resultCode, final Bundle resultData) {
               if (resultCode == 12) {
                   if (resultData == null) {
                       GroupLeaderOrNot("No message received!!!!!");
                   } else {
                       final TextView temp = (TextView) findViewById(R.id.groupLeader);

                       temp.post(new Runnable() {
                           @Override
                           public void run() {
                               temp.setText((String) resultData.get("message"));
                           }
                       });
                   }
               }
           }
        });
        startService(DeviceFuncIntent);
    }

    public void SetWifiStatus(String msg){
        TextView stausbox = (TextView) findViewById(R.id.wifistatus);
        stausbox.setText(msg);
    }
    public void SetWifiConnectStatus(String msg){
        TextView con = (TextView) findViewById(R.id.connect);
        con.setText(msg);
    }
    public void GroupLeaderOrNot(String msg){
        TextView gro = (TextView) findViewById(R.id.groupLeader);
        gro.setText(msg);
    }

}