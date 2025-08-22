package com.github.jeffreyjpz.timestamped_for_f1_web_api.web.v1.circuits.types;

public enum CircuitLocationType {

    TURN {
        @Override
        public String toString() {
            return "turn";
        }
    },
    MARSHAL_SECTOR {
        @Override
        public String toString() {
            return "marshal-sector";
        }
    },
    MINI_SECTOR {
        @Override
        public String toString() {
            return "mini-sector";
        }
    }
    
}
