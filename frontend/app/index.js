import { Link } from "expo-router";
import { Button, Text, View } from "react-native";
import AsyncStorage from "@react-native-async-storage/async-storage";
import React, { useEffect, useState } from "react";
import { useRouter } from "expo-router";

export default function Page() {
  const router = useRouter();
  const [response, setResponse] = useState(null);

  useEffect(() => {
    const checkAccessToken = async () => {
      try {
        const access_token = await AsyncStorage.getItem("access_token");

        if (!access_token) {
          // Access token is not present, navigate to login screen
          router.replace("/login");
          return;
        }

        const response = await fetch(
          "https://25ed-102-88-34-41.ngrok-free.app/user",
          {
            headers: {
              Authorization: `Bearer ${access_token}`,
            },
          }
        );

        if (!response.ok) {
          router.replace("/login");
        } else {
          // Access token is valid, display the protected page
          const data = await response.json();
          console.log(data);
          setResponse(data);
        }
      } catch (error) {
        console.error("Error:", error);
      }
    };
    checkAccessToken();
  }, []);

  const addBook = () => {
    router.replace("/addBook");
  };

  return (
    <>
      <View
        style={{
          backgroundColor: "#000",
          flex: 1,
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        {response && (
          <Text style={{ color: "#fff", marginBottom: 20, fontSize: 30 }}>
            Hi {response.logged_in_as}👋
          </Text>
        )}

        <Button
          title="Add Book"
          color="#9C00E4"
          onPress={async () => {
            <Text>Hi User</Text>;

            addBook();
          }}
        />
        <Button
          title="Logout"
          color="#9C00E4"
          onPress={async () => {
            await AsyncStorage.removeItem("access_token");

            router.replace("/login");
          }}
        />
        {!response && <Link href="/login">Login</Link>}
      </View>
    </>
  );
}
