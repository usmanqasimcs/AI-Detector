import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';
import { useThemeColor } from '@/hooks/useThemeColor';
import axios from 'axios';
import { LinearGradient } from 'expo-linear-gradient';
import React, { useState } from 'react';
import {
  ActivityIndicator,
  Alert,
  Dimensions,
  ScrollView,
  StyleSheet,
  TextInput,
  TouchableOpacity
} from 'react-native';

interface DetectionResult {
  prediction: 'Human' | 'AI';
  confidence: number;
}

const { width, height } = Dimensions.get('window');

export default function AITextDetectorScreen() {
  const [inputText, setInputText] = useState('');
  const [result, setResult] = useState<DetectionResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const backgroundColor = useThemeColor({}, 'background');
  const textColor = useThemeColor({}, 'text');
  const cardColor = useThemeColor({ light: '#ffffff', dark: '#1a1a1a' }, 'background');

  const analyzeText = async () => {
    if (!inputText.trim()) {
      Alert.alert('Error', 'Please enter some text to analyze');
      return;
    }

    setIsLoading(true);
    try {
      const response = await axios.post('http://192.168.128.108:8000/detect', {
        text: inputText
      });
      
      setResult(response.data);
    } catch (error) {
      console.error('Error analyzing text:', error);
      Alert.alert(
        'Error', 
        'Failed to analyze text. Please make sure your FastAPI server is running.'
      );
    } finally {
      setIsLoading(false);
    }
  };

  const clearAll = () => {
    setInputText('');
    setResult(null);
  };

  const getResultColor = (prediction: string) => {
    return prediction === 'Human' ? '#4CAF50' : '#FF5722';
  };

  const getConfidenceLevel = (confidence: number) => {
    if (confidence >= 90) return 'Very High';
    if (confidence >= 75) return 'High';
    if (confidence >= 60) return 'Medium';
    return 'Low';
  };

  return (
    <ScrollView style={[styles.container, { backgroundColor }]} showsVerticalScrollIndicator={false}>
      <LinearGradient
        colors={['#667eea', '#764ba2']}
        style={styles.header}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 1 }}
      >
        <ThemedText style={styles.headerTitle}>AI Text Detector</ThemedText>
        <ThemedText style={styles.headerSubtitle}>
          Detect if text is written by AI or Human
        </ThemedText>
      </LinearGradient>

      <ThemedView style={[styles.content, { backgroundColor }]}>
        <ThemedView style={[styles.card, { backgroundColor: cardColor }]}>
          <ThemedText style={styles.sectionTitle}>Enter Text to Analyze</ThemedText>
          <TextInput
            style={[styles.textInput, { 
              color: textColor,
              borderColor: useThemeColor({ light: '#e0e0e0', dark: '#333' }, 'text'),
              backgroundColor: useThemeColor({ light: '#f8f9fa', dark: '#2a2a2a' }, 'background')
            }]}
            multiline
            numberOfLines={6}
            placeholder="Paste or type the text you want to analyze..."
            placeholderTextColor={useThemeColor({ light: '#999', dark: '#666' }, 'text')}
            value={inputText}
            onChangeText={setInputText}
            textAlignVertical="top"
          />
          
          <ThemedView style={styles.buttonContainer}>
            <TouchableOpacity
              style={[styles.button, styles.primaryButton]}
              onPress={analyzeText}
              disabled={isLoading || !inputText.trim()}
            >
              {isLoading ? (
                <ActivityIndicator color="#fff" size="small" />
              ) : (
                <ThemedText style={styles.buttonText}>Analyze Text</ThemedText>
              )}
            </TouchableOpacity>

            <TouchableOpacity
              style={[styles.button, styles.secondaryButton]}
              onPress={clearAll}
              disabled={isLoading}
            >
              <ThemedText style={[styles.buttonText, { color: '#667eea' }]}>Clear</ThemedText>
            </TouchableOpacity>
          </ThemedView>
        </ThemedView>

        {result && (
          <ThemedView style={[styles.card, styles.resultCard, { backgroundColor: cardColor }]}>
            <ThemedText style={styles.sectionTitle}>Analysis Result</ThemedText>
            
            <ThemedView style={styles.resultContainer}>
              <ThemedView style={styles.predictionContainer}>
                <ThemedText style={styles.resultLabel}>Prediction:</ThemedText>
                <ThemedView style={[styles.predictionBadge, { backgroundColor: getResultColor(result.prediction) }]}>
                  <ThemedText style={styles.predictionText}>{result.prediction}</ThemedText>
                </ThemedView>
              </ThemedView>

              <ThemedView style={styles.confidenceContainer}>
                <ThemedText style={styles.resultLabel}>Confidence Score:</ThemedText>
                <ThemedView style={styles.confidenceRow}>
                  <ThemedText style={[styles.confidenceScore, { color: getResultColor(result.prediction) }]}>
                    {result.confidence.toFixed(1)}%
                  </ThemedText>
                  <ThemedText style={styles.confidenceLevel}>
                    ({getConfidenceLevel(result.confidence)})
                  </ThemedText>
                </ThemedView>
              </ThemedView>

              <ThemedView style={styles.progressBarContainer}>
                <ThemedView style={[styles.progressBar, { backgroundColor: useThemeColor({ light: '#e0e0e0', dark: '#333' }, 'text') }]}>
                  <ThemedView 
                    style={[
                      styles.progressFill, 
                      { 
                        width: `${result.confidence}%`,
                        backgroundColor: getResultColor(result.prediction)
                      }
                    ]} 
                  />
                </ThemedView>
              </ThemedView>
            </ThemedView>
          </ThemedView>
        )}

        <ThemedView style={[styles.card, { backgroundColor: cardColor }]}>
          <ThemedText style={styles.sectionTitle}>How it works</ThemedText>
          <ThemedText style={styles.infoText}>
            Our AI detection model analyzes text patterns, style, and linguistic features to determine
            whether the content was likely generated by artificial intelligence or written by a human.
          </ThemedText>
          <ThemedText style={styles.infoText}>
            The confidence score indicates how certain the model is about its prediction.
          </ThemedText>
        </ThemedView>
      </ThemedView>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  header: {
    paddingTop: 60,
    paddingBottom: 30,
    paddingHorizontal: 20,
    alignItems: 'center',
  },
  headerTitle: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#fff',
    textAlign: 'center',
    marginBottom: 8,
  },
  headerSubtitle: {
    fontSize: 16,
    color: '#fff',
    textAlign: 'center',
    opacity: 0.9,
  },
  content: {
    flex: 1,
    padding: 16,
    marginTop: -20,
    borderTopLeftRadius: 20,
    borderTopRightRadius: 20,
  },
  card: {
    borderRadius: 16,
    padding: 20,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 4,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    marginBottom: 16,
  },
  textInput: {
    borderWidth: 1,
    borderRadius: 12,
    padding: 16,
    fontSize: 16,
    lineHeight: 24,
    minHeight: 120,
    marginBottom: 20,
  },
  buttonContainer: {
    flexDirection: 'row',
    gap: 12,
  },
  button: {
    flex: 1,
    paddingVertical: 16,
    paddingHorizontal: 24,
    borderRadius: 12,
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: 50,
  },
  primaryButton: {
    backgroundColor: '#667eea',
  },
  secondaryButton: {
    backgroundColor: 'transparent',
    borderWidth: 2,
    borderColor: '#667eea',
  },
  buttonText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#fff',
  },
  resultCard: {
    borderLeftWidth: 4,
    borderLeftColor: '#667eea',
  },
  resultContainer: {
    gap: 20,
  },
  predictionContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  resultLabel: {
    fontSize: 16,
    fontWeight: '500',
  },
  predictionBadge: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
  },
  predictionText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  confidenceContainer: {
    gap: 8,
  },
  confidenceRow: {
    flexDirection: 'row',
    alignItems: 'baseline',
    gap: 8,
  },
  confidenceScore: {
    fontSize: 24,
    fontWeight: 'bold',
  },
  confidenceLevel: {
    fontSize: 14,
    opacity: 0.7,
  },
  progressBarContainer: {
    marginTop: 8,
  },
  progressBar: {
    height: 8,
    borderRadius: 4,
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    borderRadius: 4,
  },
  infoText: {
    fontSize: 14,
    lineHeight: 20,
    opacity: 0.8,
    marginBottom: 8,
  },
});
