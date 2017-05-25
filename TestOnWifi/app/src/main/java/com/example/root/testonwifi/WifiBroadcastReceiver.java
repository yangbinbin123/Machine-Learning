package com.example.root.testonwifi;

/**
 * Created by LINBIN on 17-5-23.
 */
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.net.NetworkInfo;
import android.net.wifi.p2p.WifiP2pDevice;
import android.net.wifi.p2p.WifiP2pDeviceList;
import android.net.wifi.p2p.WifiP2pInfo;
import android.net.wifi.p2p.WifiP2pManager;
import android.net.wifi.p2p.WifiP2pManager.Channel;

public class WifiBroadcastReceiver extends BroadcastReceiver{
    private WifiP2pManager manager;
    private Channel channel;
    private MainActivity activity;

    public WifiBroadcastReceiver(WifiP2pManager manager, Channel channel, MainActivity activity){
        super();
        this.manager = manager;
        this.channel = channel;
        this.activity = activity;
        //activity.setServerStatus("BroastCast start");
    }
    @Override
    public void onReceive(Context context, Intent intent){
        final String action = intent.getAction();
        if (WifiP2pManager.WIFI_P2P_STATE_CHANGED_ACTION.equals(action)) {
            int state = intent.getIntExtra(WifiP2pManager.EXTRA_WIFI_STATE,-1);
            if (state == WifiP2pManager.WIFI_P2P_STATE_ENABLED){
                activity.SetWifiStatus("WifiP2P is enabled!");
            }
            else{
                activity.SetWifiStatus("WifiP2P is not enabled");
            }
        }
        else if (WifiP2pManager.WIFI_P2P_PEERS_CHANGED_ACTION.equals(action)) {
            // Call WifiP2pManager.requestPeers() to get a list of current peers
            manager.requestPeers(channel, new WifiP2pManager.PeerListListener(){
                public void onPeersAvailable(WifiP2pDeviceList peers){
                    activity.displayPeers(peers);
                }
            });
        }
        else if (WifiP2pManager.WIFI_P2P_CONNECTION_CHANGED_ACTION.equals(action)) {
            // Respond to new connection or disconnections
            NetworkInfo networkState = intent.getParcelableExtra(WifiP2pManager.EXTRA_NETWORK_INFO);
            WifiP2pInfo wifiInfo = intent.getParcelableExtra(WifiP2pManager.EXTRA_WIFI_P2P_INFO);
            WifiP2pDevice device = intent.getParcelableExtra(WifiP2pManager.EXTRA_WIFI_P2P_DEVICE);

            if(networkState.isConnected()){
                activity.setNetworkToReadyState(wifiInfo,device);
                activity.SetWifiConnectStatus("Connected!!!!!");
            }
            else{
                activity.SetWifiConnectStatus("Not Connected!!!!!");
                manager.cancelConnect(channel,null);
            }
        }
        else if (WifiP2pManager.WIFI_P2P_THIS_DEVICE_CHANGED_ACTION.equals(action)) {
            // Respond to this device's wifi state changing
        }
    }
}
