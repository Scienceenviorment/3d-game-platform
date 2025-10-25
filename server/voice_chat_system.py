"""
Voice Chat System - Real-time voice communication with NPCs and players
Supports speech-to-text for NPC interactions and voice chat between players
"""

import asyncio
import json
import base64
import wave
import io
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum

class VoiceChannelType(Enum):
    GLOBAL = "global"
    LOCAL = "local"
    PARTY = "party"
    NPC_INTERACTION = "npc_interaction"
    PRIVATE = "private"

@dataclass
class VoiceMessage:
    sender_id: str
    sender_name: str
    channel: VoiceChannelType
    audio_data: str  # Base64 encoded audio
    transcript: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    target_id: Optional[str] = None  # For private messages or NPC interactions

@dataclass
class VoiceChannel:
    channel_id: str
    channel_type: VoiceChannelType
    participants: List[str] = field(default_factory=list)
    is_active: bool = True
    max_participants: int = 50

class VoiceChatSystem:
    def __init__(self):
        self.voice_channels: Dict[str, VoiceChannel] = {}
        self.player_voice_settings: Dict[str, Dict[str, Any]] = {}
        self.active_conversations: Dict[str, str] = {}  # player_id -> npc_id
        self.voice_history: List[VoiceMessage] = []
        
        # Initialize default channels
        self._create_default_channels()
    
    def _create_default_channels(self):
        """Create default voice channels"""
        self.voice_channels["global"] = VoiceChannel(
            channel_id="global",
            channel_type=VoiceChannelType.GLOBAL,
            max_participants=100
        )
        
        self.voice_channels["local"] = VoiceChannel(
            channel_id="local", 
            channel_type=VoiceChannelType.LOCAL,
            max_participants=20
        )
    
    async def join_voice_channel(self, player_id: str, channel_id: str) -> Dict[str, Any]:
        """Join a voice channel"""
        if channel_id not in self.voice_channels:
            return {"error": "Voice channel not found"}
        
        channel = self.voice_channels[channel_id]
        
        if len(channel.participants) >= channel.max_participants:
            return {"error": "Voice channel is full"}
        
        if player_id not in channel.participants:
            channel.participants.append(player_id)
        
        return {
            "success": True,
            "channel_id": channel_id,
            "channel_type": channel.channel_type.value,
            "participants": channel.participants,
            "message": f"Joined voice channel: {channel_id}"
        }
    
    async def leave_voice_channel(self, player_id: str, channel_id: str) -> Dict[str, Any]:
        """Leave a voice channel"""
        if channel_id in self.voice_channels:
            channel = self.voice_channels[channel_id]
            if player_id in channel.participants:
                channel.participants.remove(player_id)
        
        return {"success": True, "message": f"Left voice channel: {channel_id}"}
    
    async def send_voice_message(self, sender_id: str, sender_name: str, 
                                audio_data: str, channel_id: str, 
                                target_id: Optional[str] = None) -> Dict[str, Any]:
        """Send a voice message to a channel"""
        
        if channel_id not in self.voice_channels:
            return {"error": "Voice channel not found"}
        
        channel = self.voice_channels[channel_id]
        
        # Create voice message
        voice_msg = VoiceMessage(
            sender_id=sender_id,
            sender_name=sender_name,
            channel=channel.channel_type,
            audio_data=audio_data,
            target_id=target_id
        )
        
        # Add to history
        self.voice_history.append(voice_msg)
        
        # Prepare message for distribution
        message_data = {
            "type": "voice_message",
            "sender_id": sender_id,
            "sender_name": sender_name,
            "channel": channel_id,
            "audio_data": audio_data,
            "timestamp": voice_msg.timestamp.isoformat(),
            "target_id": target_id
        }
        
        return {
            "success": True,
            "message_data": message_data,
            "recipients": channel.participants if not target_id else [target_id]
        }
    
    async def start_npc_conversation(self, player_id: str, npc_id: str) -> Dict[str, Any]:
        """Start a voice conversation with an NPC"""
        
        # Create dedicated NPC conversation channel
        conversation_id = f"npc_{player_id}_{npc_id}"
        
        self.voice_channels[conversation_id] = VoiceChannel(
            channel_id=conversation_id,
            channel_type=VoiceChannelType.NPC_INTERACTION,
            participants=[player_id],
            max_participants=2
        )
        
        self.active_conversations[player_id] = npc_id
        
        return {
            "success": True,
            "conversation_id": conversation_id,
            "npc_id": npc_id,
            "message": f"Started voice conversation with {npc_id}",
            "instructions": {
                "speak_to_activate": "Press and hold SPACE to speak",
                "auto_translate": "Your speech will be converted to text for the NPC",
                "npc_responses": "NPC responses will be both text and synthesized voice"
            }
        }
    
    async def end_npc_conversation(self, player_id: str) -> Dict[str, Any]:
        """End voice conversation with NPC"""
        
        if player_id in self.active_conversations:
            npc_id = self.active_conversations[player_id]
            conversation_id = f"npc_{player_id}_{npc_id}"
            
            # Remove conversation channel
            if conversation_id in self.voice_channels:
                del self.voice_channels[conversation_id]
            
            del self.active_conversations[player_id]
            
            return {
                "success": True,
                "message": f"Ended conversation with {npc_id}"
            }
        
        return {"error": "No active NPC conversation"}
    
    async def process_speech_to_text(self, audio_data: str) -> Dict[str, Any]:
        """Convert speech to text for NPC interactions"""
        
        # In a real implementation, this would use a speech recognition service
        # For demo purposes, we'll simulate speech recognition
        
        # Decode base64 audio (this would normally go to speech recognition API)
        try:
            audio_bytes = base64.b64decode(audio_data)
            
            # Simulate speech recognition processing
            await asyncio.sleep(0.5)  # Simulate processing time
            
            # Mock transcription (in reality, use services like Google Speech-to-Text, Azure Speech, etc.)
            mock_transcriptions = [
                "Hello, what can you tell me about the ancient beasts?",
                "I want to learn about taming Garuda.",
                "Can you teach me about the sacred rituals?",
                "What do you know about the dimensional collision?",
                "How can I improve my karma?",
                "Tell me about the secret shrine.",
                "I need help with beast taming.",
                "What powers can I gain from the gods?"
            ]
            
            import random
            transcript = random.choice(mock_transcriptions)
            
            return {
                "success": True,
                "transcript": transcript,
                "confidence": 0.95,
                "processing_time": 0.5
            }
            
        except Exception as e:
            return {
                "error": f"Speech recognition failed: {str(e)}",
                "fallback": "Please use text input"
            }
    
    async def synthesize_npc_speech(self, text: str, npc_id: str) -> Dict[str, Any]:
        """Convert NPC text responses to speech"""
        
        # In a real implementation, this would use text-to-speech services
        # For demo purposes, we'll simulate TTS
        
        try:
            # Simulate TTS processing
            await asyncio.sleep(0.3)
            
            # Mock audio generation (in reality, use services like Azure Speech, AWS Polly, etc.)
            # This would return actual audio data
            mock_audio = base64.b64encode(b"mock_audio_data_for_" + text.encode()).decode()
            
            return {
                "success": True,
                "audio_data": mock_audio,
                "text": text,
                "voice_type": self._get_npc_voice_type(npc_id),
                "duration": len(text) * 0.1  # Rough estimate
            }
            
        except Exception as e:
            return {
                "error": f"Speech synthesis failed: {str(e)}",
                "fallback_text": text
            }
    
    def _get_npc_voice_type(self, npc_id: str) -> str:
        """Get appropriate voice type for each NPC"""
        voice_types = {
            "arunima": "female_scholarly_calm",
            "devraj": "male_adventurous_confident", 
            "rukmini": "female_elderly_wise",
            "void_keeper": "male_otherworldly_deep",
            "lyralei": "female_ethereal_melodic",
            "valdris": "male_dark_commanding",
            "seraphina": "female_divine_harmonious"
        }
        
        return voice_types.get(npc_id, "neutral")
    
    def get_voice_settings(self, player_id: str) -> Dict[str, Any]:
        """Get player's voice settings"""
        return self.player_voice_settings.get(player_id, {
            "microphone_enabled": True,
            "voice_activation": True,
            "push_to_talk_key": "SPACE",
            "volume_input": 0.8,
            "volume_output": 0.8,
            "noise_suppression": True,
            "echo_cancellation": True,
            "voice_effects": False,
            "preferred_language": "en-US",
            "npc_voice_enabled": True,
            "auto_transcript": True
        })
    
    def update_voice_settings(self, player_id: str, settings: Dict[str, Any]) -> Dict[str, Any]:
        """Update player's voice settings"""
        current_settings = self.get_voice_settings(player_id)
        current_settings.update(settings)
        self.player_voice_settings[player_id] = current_settings
        
        return {
            "success": True,
            "settings": current_settings,
            "message": "Voice settings updated"
        }
    
    def get_voice_status(self) -> Dict[str, Any]:
        """Get overall voice system status"""
        return {
            "total_channels": len(self.voice_channels),
            "active_conversations": len(self.active_conversations),
            "total_participants": sum(len(ch.participants) for ch in self.voice_channels.values()),
            "voice_history_count": len(self.voice_history),
            "features": {
                "speech_to_text": True,
                "text_to_speech": True,
                "real_time_voice": True,
                "npc_conversations": True,
                "multi_channel": True,
                "noise_suppression": True
            }
        }

# Test the voice system
async def test_voice_system():
    """Test voice chat functionality"""
    voice_system = VoiceChatSystem()
    
    print("=== VOICE CHAT SYSTEM TEST ===\n")
    
    # Test joining voice channel
    print("1. Testing voice channel join...")
    join_result = await voice_system.join_voice_channel("player1", "global")
    print(f"Join result: {join_result}")
    
    # Test NPC conversation
    print("\n2. Testing NPC conversation...")
    npc_conv = await voice_system.start_npc_conversation("player1", "arunima")
    print(f"NPC conversation: {npc_conv}")
    
    # Test speech to text
    print("\n3. Testing speech recognition...")
    mock_audio = base64.b64encode(b"mock_audio_hello_npc").decode()
    speech_result = await voice_system.process_speech_to_text(mock_audio)
    print(f"Speech recognition: {speech_result}")
    
    # Test text to speech
    print("\n4. Testing NPC voice synthesis...")
    tts_result = await voice_system.synthesize_npc_speech(
        "Namaste, young seeker. I can sense great potential in you for beast taming.", 
        "arunima"
    )
    print(f"TTS result: {tts_result}")
    
    # Test voice settings
    print("\n5. Testing voice settings...")
    settings = voice_system.get_voice_settings("player1")
    print(f"Default settings: {settings}")
    
    # Test system status
    print("\n6. Voice system status...")
    status = voice_system.get_voice_status()
    print(f"System status: {status}")

if __name__ == "__main__":
    asyncio.run(test_voice_system())