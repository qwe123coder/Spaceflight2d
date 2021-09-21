def SaveSettings():
    f = open(savedir + "settings", "w")
    f.write(
        "Sound Volume\n\tMusic: %d\n\tEffects: %d\n"
        "Keys\n\tUp: %d\n\tLeft: %d\n\tRight: %d\n\tFire: %d\n\tLaunch: %d\n\tBuild: %d\n\tRepair: %d\n\tFill: %d\n\tPause: %d\n\tZoomOut: %d\n"
        "\tZoomIn: %d\n\tDrop: %d\n\tMap: %d\n\tExVis: %d\nScreen\n\tMode: %s\n\tSize: %s\n"
        % (
            MUSIC_VOLUME,
            FX_VOLUME,
            KEYS["UP"],
            KEYS["LEFT"],
            KEYS["RIGHT"],
            KEYS["FIRE"],
            KEYS["LAUNCH"],
            KEYS["BUILD"],
            KEYS["REPAIR"],
            KEYS["FILL"],
            KEYS["PAUSE"],
            KEYS["ZOOMOUT"],
            KEYS["ZOOMIN"],
            KEYS["DROP"],
            KEYS["MAP"],
            KEYS["EXVIS"],
            "Full" if SCR_FULL else "Windowed",
            "x".join(str(i) for i in SCR_SIZE),
        )
    )
    f.close()
