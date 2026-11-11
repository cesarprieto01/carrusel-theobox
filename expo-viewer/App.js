// Theo · visor del prototipo para Expo Go.
// Carga el home de Theo con la sección TheoBox publicado en Vercel, a pantalla completa.
import { useState } from 'react';
import { View, Text, Pressable, StyleSheet } from 'react-native';
import { WebView } from 'react-native-webview';
import { StatusBar } from 'expo-status-bar';
import * as ScreenOrientation from 'expo-screen-orientation';

const URL = 'https://theo-home-theobox.vercel.app/theobox.html?app=1';

export default function App() {
  const [error, setError] = useState(false);
  const [key, setKey] = useState(0);
  if (error) {
    return (
      <View style={s.err}>
        <Text style={s.errT}>No encuentro el prototipo</Text>
        <Text style={s.errM}>Revisa la conexión a internet del teléfono.</Text>
        <Pressable style={s.btn} onPress={() => { setError(false); setKey(k => k + 1); }}><Text style={s.btnT}>Reintentar</Text></Pressable>
      </View>
    );
  }
  return (
    <View style={{ flex: 1, backgroundColor: '#D8F6F8' }}>
      <StatusBar style="dark" />
      <WebView
        key={key}
        source={{ uri: URL + '&t=' + Date.now() }}
        style={{ flex: 1, backgroundColor: '#D8F6F8' }}
        originWhitelist={['*']}
        allowsInlineMediaPlayback
        mediaPlaybackRequiresUserAction={false}
        bounces={false}
        overScrollMode="never"
        cacheEnabled={false}
        contentInsetAdjustmentBehavior="never"
        onMessage={e => {
          // el prototipo avisa al abrir y cerrar un video: los videos solo se ven en horizontal
          const m = e.nativeEvent.data;
          if (m === 'video:on') ScreenOrientation.lockAsync(ScreenOrientation.OrientationLock.LANDSCAPE).catch(() => {});
          if (m === 'video:off') ScreenOrientation.unlockAsync().catch(() => {});
        }}
        onError={() => setError(true)}
        onHttpError={() => setError(true)}
      />
    </View>
  );
}

const s = StyleSheet.create({
  err: { flex: 1, backgroundColor: '#00082B', alignItems: 'center', justifyContent: 'center', padding: 32 },
  errT: { color: '#FCFBF7', fontSize: 20, fontWeight: '800', marginBottom: 8 },
  errM: { color: '#B9C3D9', fontSize: 15, textAlign: 'center', lineHeight: 22, marginBottom: 24 },
  btn: { backgroundColor: '#F5DB78', borderRadius: 999, paddingHorizontal: 24, paddingVertical: 14 },
  btnT: { color: '#02254F', fontWeight: '800', fontSize: 16 },
});
