# FOR MULTIPLE USERS
data = [
    {
        "accessPoints": [
            {
                "ssid": 'ssid1',
                "bssid": 'bssid1',
                "signalStrength": -20,
                "frequency": 5040
            },
            {
                "ssid": 'ssid1',
                "bssid": 'bssid2',
                "signalStrength": -60,
                "frequency": 5040
            },
            {
                "ssid": 'ssid1',
                "bssid": 'bssid3',
                "signalStrength": -60,
                "frequency": 5040
            },
        ],
        "user": "john doe"
    },
    {
        "accessPoints": [
            {
                "ssid": 'ssid2',
                "bssid": 'bssid4',
                "signalStrength": -30,
                "frequency": 2412
            },
            {
                "ssid": 'ssid2',
                "bssid": 'bssid5',
                "signalStrength": -50,
                "frequency": 2412
            },
            {
                "ssid": 'ssid2',
                "bssid": 'bssid6',
                "signalStrength": -70,
                "frequency": 2412
            },
        ],
        "user": "jane smith"
    },
    {
        "accessPoints": [
            {
                "ssid": 'ssid3',
                "bssid": 'bssid7',
                "signalStrength": -40,
                "frequency": 5180
            },
            {
                "ssid": 'ssid3',
                "bssid": 'bssid8',
                "signalStrength": -80,
                "frequency": 5180
            },
            {
                "ssid": 'ssid3',
                "bssid": 'bssid9',
                "signalStrength": -90,
                "frequency": 5180
            },
        ],
        "user": "alex lee"
    }
]

# DATA VARIANTS FOR DISCOVERING APs
# Original data
data_variant_1 = {
    "accessPoints": [
        {
            "ssid": 'ssid1',
            "bssid": 'bssid1',
            "signalStrength": -20,
            "frequency": 5040
        },
        {
            "ssid": 'ssid1',
            "bssid": 'bssid2',
            "signalStrength": -60,
            "frequency": 5040
        },
        {
            "ssid": 'ssid1',
            "bssid": 'bssid3',
            "signalStrength": -60,
            "frequency": 5040
        },
    ],
    "user": "john doe"
}

# First variant with different signal strength values
data_variant_2 = {
    "accessPoints": [
        {
            "ssid": 'ssid1',
            "bssid": 'bssid1',
            "signalStrength": -25,
            "frequency": 5040
        },
        {
            "ssid": 'ssid1',
            "bssid": 'bssid2',
            "signalStrength": -55,
            "frequency": 5040
        },
        {
            "ssid": 'ssid1',
            "bssid": 'bssid3',
            "signalStrength": -65,
            "frequency": 5040
        },
    ],
    "user": "john doe"
}

# Second variant with different signal strength values
data_variant_3 = {
    "accessPoints": [
        {
            "ssid": 'ssid1',
            "bssid": 'bssid1',
            "signalStrength": -30,
            "frequency": 5040
        },
        {
            "ssid": 'ssid1',
            "bssid": 'bssid2',
            "signalStrength": -50,
            "frequency": 5040
        },
        {
            "ssid": 'ssid1',
            "bssid": 'bssid3',
            "signalStrength": -70,
            "frequency": 5040
        },
    ],
    "user": "john doe"
}

# Combine all variants into one list if needed
data_variants = [data_variant_1, data_variant_2, data_variant_3]
