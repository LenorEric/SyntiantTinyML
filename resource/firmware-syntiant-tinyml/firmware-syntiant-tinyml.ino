#include "src/syntiant.h"
#include <NDP.h>
#include <NDP_utils.h>
#include <Arduino.h>

extern int light;
extern int awake;

/**
 * @brief      Called when a inference matches 1 of the features
 *
 * @param[in]  event          The event
 * @param[in]  confidence     The confidence
 * @param[in]  anomaly_score  The anomaly score
 */
void on_classification_changed(const char *event, float confidence, float anomaly_score) {
    if (strcmp(event, "awake") == 0) {
        awake = 1;
        light = 0;
        return;
    }

    if (strcmp(event, "light") == 0 && awake) {
        light = 1;
        awake = 0;
        return;
    }
    if (strcmp(event, "shut") == 0 && awake) {
        light = 0;
        awake = 0;
        return;
    }
    if (strcmp(event, "blink") == 0 && awake) {
        light = 2;
        awake = 0;
        return;
    }
}



void setup(void)
{
    syntiant_setup();
}

void loop(void)
{
    syntiant_loop();
}
